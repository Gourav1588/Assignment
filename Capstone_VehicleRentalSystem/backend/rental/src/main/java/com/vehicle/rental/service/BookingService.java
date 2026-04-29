package com.vehicle.rental.service;

import com.vehicle.rental.dto.request.BookingRequest;
import com.vehicle.rental.dto.response.BookingResponse;
import com.vehicle.rental.entity.Booking;
import com.vehicle.rental.entity.Booking.BookingStatus;
import com.vehicle.rental.entity.User;
import com.vehicle.rental.entity.Vehicle;
import com.vehicle.rental.exception.BadRequestException;
import com.vehicle.rental.exception.ResourceNotFoundException;
import com.vehicle.rental.exception.UnauthorizedAccessException;
import com.vehicle.rental.exception.VehicleNotAvailableException;
import com.vehicle.rental.mapper.BookingMapper;
import com.vehicle.rental.repository.BookingRepository;
import com.vehicle.rental.repository.UserRepository;
import com.vehicle.rental.repository.VehicleRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.time.temporal.ChronoUnit;

/**
 * Service layer orchestrating the core rental workflow.
 * Manages the lifecycle of a booking from creation (PENDING) through confirmation,
 * completion, or cancellation, enforcing strict temporal and financial business rules.
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class BookingService {

    private final BookingRepository bookingRepository;
    private final VehicleRepository vehicleRepository;
    private final UserRepository userRepository;
    private final BookingMapper bookingMapper;

    /**
     * Initializes a new vehicle rental request.
     * Enforces a maximum rental duration of 720 hours (30 days) and verifies the vehicle
     * is completely free during the requested timeframe.
     */
    @Transactional
    public BookingResponse createBooking(Long userId, BookingRequest request) {
        log.debug("Initiating booking creation for user ID: {}, vehicle ID: {}", userId, request.getVehicleId());

        if (request.getEndTime().isBefore(request.getStartTime())) {
            throw new BadRequestException("End time cannot precede start time");
        }

        // Calculate total hours, ensuring a minimum 1-hour block
        long totalHours = ChronoUnit.HOURS.between(request.getStartTime(), request.getEndTime());
        if (totalHours < 1) totalHours = 1;

        // 720 hours = 30 days
        if (totalHours > 720) {
            throw new BadRequestException("Booking duration exceeds the 30-day maximum limit");
        }

        Vehicle vehicle = vehicleRepository.findById(request.getVehicleId())
                .orElseThrow(() -> new ResourceNotFoundException("Requested vehicle not found"));

        if (!vehicle.isActive()) {
            throw new BadRequestException("Vehicle is currently retired or suspended from the fleet");
        }

        boolean available = bookingRepository.isVehicleAvailable(
                request.getVehicleId(), request.getStartTime(), request.getEndTime()
        );

        if (!available) {
            throw new VehicleNotAvailableException("Vehicle is already reserved for the selected times");
        }

        User user = userRepository.findById(userId)
                .orElseThrow(() -> new ResourceNotFoundException("User identity could not be verified"));

        /* =========================================================================
           PRICING MATH
           Calculates how many 24-hour blocks the user is touching and rounds up.
           E.g., 26 hours = 2 days billed.
           ========================================================================= */
        long billedDays = (long) Math.ceil((double) totalHours / 24.0);

        Booking booking = new Booking();
        booking.setUser(user);
        booking.setVehicle(vehicle);
        booking.setStartTime(request.getStartTime());
        booking.setEndTime(request.getEndTime());
        booking.setTotalCost(billedDays * vehicle.getPricePerDay());
        booking.setStatus(BookingStatus.PENDING); // Change to ACTIVE if bypassing confirmation

        return bookingMapper.toResponse(bookingRepository.save(booking));
    }

    /**
     * Transitions a pending booking into an active, confirmed rental.
     */
    @Transactional
    public BookingResponse confirmBooking(Long bookingId, Long userId) {
        Booking booking = bookingRepository.findById(bookingId)
                .orElseThrow(() -> new ResourceNotFoundException("Booking record not found"));

        if (!booking.getUser().getId().equals(userId)) {
            throw new UnauthorizedAccessException("Cannot confirm bookings belonging to other accounts");
        }

        if (booking.getStatus() != BookingStatus.PENDING) {
            throw new BadRequestException("Only PENDING bookings are eligible for confirmation");
        }

        booking.setStatus(BookingStatus.ACTIVE);
        log.info("Booking ID {} confirmed by user ID {}", bookingId, userId);

        return bookingMapper.toResponse(bookingRepository.save(booking));
    }

    /**
     * Cancels an existing booking.
     * Prevents cancellation if the current exact time is past the start time.
     */
    @Transactional
    public BookingResponse cancelBooking(Long bookingId, Long userId) {
        Booking booking = bookingRepository.findById(bookingId)
                .orElseThrow(() -> new ResourceNotFoundException("Booking record not found"));

        if (!booking.getUser().getId().equals(userId)) {
            throw new UnauthorizedAccessException("Cannot cancel bookings belonging to other accounts");
        }

        if (booking.getStatus() != BookingStatus.PENDING && booking.getStatus() != BookingStatus.ACTIVE) {
            throw new BadRequestException("Only PENDING or ACTIVE bookings can be cancelled");
        }

        // Updated to check exact time against LocalDateTime.now()
        if (booking.getStartTime().isBefore(LocalDateTime.now())) {
            throw new BadRequestException("Cancellations are not permitted after the rental start time");
        }

        booking.setStatus(BookingStatus.CANCELLED);
        log.info("Booking ID {} cancelled by user ID {}", bookingId, userId);

        return bookingMapper.toResponse(bookingRepository.save(booking));
    }

    public Page<BookingResponse> getUserBookings(Long userId, int page, int size) {
        Pageable pageable = PageRequest.of(page, size, Sort.by("createdAt").descending());
        return bookingRepository.findByUserId(userId, pageable).map(bookingMapper::toResponse);
    }

    public Page<BookingResponse> getAllBookings(int page, int size) {
        Pageable pageable = PageRequest.of(page, size, Sort.by("createdAt").descending());
        return bookingRepository.findAll(pageable).map(bookingMapper::toResponse);
    }

    public Page<BookingResponse> getBookingsByStatus(BookingStatus status, int page, int size) {
        Pageable pageable = PageRequest.of(page, size, Sort.by("createdAt").descending());
        return bookingRepository.findByStatus(status, pageable).map(bookingMapper::toResponse);
    }
}