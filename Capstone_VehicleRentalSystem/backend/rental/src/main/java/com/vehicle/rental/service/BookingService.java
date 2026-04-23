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

import java.time.LocalDate;
import java.time.temporal.ChronoUnit;

@Slf4j
@Service
@RequiredArgsConstructor
public class BookingService {

    // Repository for booking operations
    private final BookingRepository bookingRepository;

    // Repository for vehicle validation
    private final VehicleRepository vehicleRepository;

    // Repository to fetch user details
    private final UserRepository userRepository;

    // Mapper for converting entity ↔ DTO
    private final BookingMapper bookingMapper;

    // Create a new booking (initial status = PENDING)
    @Transactional
    public BookingResponse createBooking(Long userId, BookingRequest request) {

        log.debug("Creating booking for user {} vehicle {}", userId, request.getVehicleId());

        // Validate date range (end date must not be before start date)
        if (request.getEndDate().isBefore(request.getStartDate())) {
            throw new BadRequestException("End date cannot be before start date");
        }

        // Validate booking duration (max 30 days)
        long totalDays = ChronoUnit.DAYS.between(
                request.getStartDate(),
                request.getEndDate()
        ) + 1;

        if (totalDays > 30) {
            throw new BadRequestException("Booking duration cannot exceed 30 days");
        }

        // Fetch vehicle or throw exception
        Vehicle vehicle = vehicleRepository.findById(request.getVehicleId())
                .orElseThrow(() -> new ResourceNotFoundException("Vehicle not found"));

        // Ensure vehicle is active
        if (!vehicle.isActive()) {
            throw new BadRequestException("Vehicle is not available for booking");
        }

        // Check availability (no overlapping bookings)
        boolean available = bookingRepository.isVehicleAvailable(
                request.getVehicleId(),
                request.getStartDate(),
                request.getEndDate()
        );

        if (!available) {
            throw new VehicleNotAvailableException(
                    "Vehicle is already booked for the selected dates");
        }

        // Fetch user or throw exception
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new ResourceNotFoundException("User not found"));

        // Calculate total cost
        double totalCost = totalDays * vehicle.getPricePerDay();

        // Create booking entity
        Booking booking = new Booking();
        booking.setUser(user);
        booking.setVehicle(vehicle);
        booking.setStartDate(request.getStartDate());
        booking.setEndDate(request.getEndDate());
        booking.setTotalCost(totalCost);
        booking.setStatus(BookingStatus.PENDING);

        log.debug("Booking created with PENDING status");

        // Save and return response
        return bookingMapper.toResponse(
                bookingRepository.save(booking)
        );
    }

    // Confirm booking (PENDING → ACTIVE)
    @Transactional
    public BookingResponse confirmBooking(Long bookingId, Long userId) {

        log.debug("Confirming booking id: {}", bookingId);

        // Fetch booking
        Booking booking = bookingRepository.findById(bookingId)
                .orElseThrow(() -> new ResourceNotFoundException("Booking not found"));

        // Ensure booking belongs to the user
        if (!booking.getUser().getId().equals(userId)) {
            throw new UnauthorizedAccessException(
                    "You can only confirm your own bookings");
        }

        // Only pending bookings can be confirmed
        if (booking.getStatus() != BookingStatus.PENDING) {
            throw new BadRequestException(
                    "Only pending bookings can be confirmed");
        }

        // Update status
        booking.setStatus(BookingStatus.ACTIVE);

        log.debug("Booking {} confirmed successfully", bookingId);

        return bookingMapper.toResponse(
                bookingRepository.save(booking)
        );
    }

    // Cancel booking (PENDING/ACTIVE → CANCELLED)
    @Transactional
    public BookingResponse cancelBooking(Long bookingId, Long userId) {

        log.debug("Cancelling booking id: {}", bookingId);

        // Fetch booking
        Booking booking = bookingRepository.findById(bookingId)
                .orElseThrow(() -> new ResourceNotFoundException("Booking not found"));

        // Ensure booking belongs to the user
        if (!booking.getUser().getId().equals(userId)) {
            throw new UnauthorizedAccessException(
                    "You can only cancel your own bookings");
        }

        // Only pending or active bookings can be cancelled
        if (booking.getStatus() != BookingStatus.PENDING &&
                booking.getStatus() != BookingStatus.ACTIVE) {
            throw new BadRequestException(
                    "Only pending or active bookings can be cancelled");
        }

        // Prevent cancellation if booking has already started
        if (booking.getStartDate().isBefore(LocalDate.now())) {
            throw new BadRequestException(
                    "Cannot cancel a booking that has already started");
        }

        // Update status
        booking.setStatus(BookingStatus.CANCELLED);

        log.debug("Booking {} cancelled successfully", bookingId);

        return bookingMapper.toResponse(
                bookingRepository.save(booking)
        );
    }

    // Fetch bookings of a specific user (with pagination)
    public Page<BookingResponse> getUserBookings(Long userId, int page, int size) {

        Pageable pageable = PageRequest.of(
                page, size, Sort.by("createdAt").descending()
        );

        return bookingRepository
                .findByUserId(userId, pageable)
                .map(bookingMapper::toResponse);
    }

    // Fetch all bookings (admin use)
    public Page<BookingResponse> getAllBookings(int page, int size) {

        Pageable pageable = PageRequest.of(
                page, size, Sort.by("createdAt").descending()
        );

        return bookingRepository
                .findAll(pageable)
                .map(bookingMapper::toResponse);
    }

    // Fetch bookings filtered by status (admin use)
    public Page<BookingResponse> getBookingsByStatus(
            BookingStatus status, int page, int size) {

        Pageable pageable = PageRequest.of(
                page, size, Sort.by("createdAt").descending()
        );

        return bookingRepository
                .findByStatus(status, pageable)
                .map(bookingMapper::toResponse);
    }
}