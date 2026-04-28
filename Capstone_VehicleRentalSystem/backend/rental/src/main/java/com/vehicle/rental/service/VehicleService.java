package com.vehicle.rental.service;

import com.vehicle.rental.dto.request.VehicleRequest;
import com.vehicle.rental.dto.response.VehicleResponse;
import com.vehicle.rental.entity.Booking.BookingStatus;
import com.vehicle.rental.entity.Vehicle;
import com.vehicle.rental.entity.Vehicle.VehicleType;
import com.vehicle.rental.exception.BadRequestException;
import com.vehicle.rental.exception.ResourceNotFoundException;
import com.vehicle.rental.mapper.VehicleMapper;
import com.vehicle.rental.repository.BookingRepository;
import com.vehicle.rental.repository.VehicleRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.*;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.util.List;

@Slf4j // Logging support
@Service // Service layer
@RequiredArgsConstructor
public class VehicleService {

    private final VehicleRepository vehicleRepository; // DB access
    private final BookingRepository bookingRepository; // Booking checks
    private final CategoryService categoryService; // Category fetch
    private final VehicleMapper vehicleMapper; // DTO mapper

    // Fetch vehicles with filters + pagination
    public Page<VehicleResponse> getVehicles(
            int page, int size,
            VehicleType type,
            Long categoryId,
            String name) {

        // Validate pagination inputs
        if (page < 0) throw new BadRequestException("Page cannot be negative");
        if (size <= 0) throw new BadRequestException("Size must be > 0");

        // Create pageable (latest first)
        Pageable pageable = PageRequest.of(
                page, size, Sort.by("createdAt").descending()
        );

        // Apply filters (ignore null/blank values)
        return vehicleRepository
                .findAllWithFilters(
                        name != null && !name.isBlank() ? name : "",
                        type,
                        categoryId,
                        pageable
                )
                .map(vehicleMapper::toResponse); // Convert to DTO
    }

    // Get single vehicle by id
    public VehicleResponse getVehicleById(Long id) {
        Vehicle vehicle = vehicleRepository.findById(id)
                .orElseThrow(() ->
                        new ResourceNotFoundException("Vehicle not found"));

        return vehicleMapper.toResponse(vehicle); // Map to DTO
    }

    // Create new vehicle
    @Transactional
    public VehicleResponse createVehicle(VehicleRequest request) {
        String normalizedName = request.getName().trim();
        String normalizedPlate = request.getRegistrationNumber().trim();


        // Prevent duplicate Registration Numbers ---
        if (vehicleRepository.existsByRegistrationNumberIgnoreCase(normalizedPlate)) {
            throw new BadRequestException("A vehicle with registration number " + normalizedPlate + " already exists in the fleet.");
        }

        // Convert DTO → entity
        Vehicle vehicle = vehicleMapper.toEntity(request);
        vehicle.setName(normalizedName); // Ensure clean name
        // (Note: vehicleMapper.toEntity already sets the registrationNumber)

        // Attach category if provided
        if (request.getCategoryId() != null) {
            vehicle.setCategory(
                    categoryService.getCategoryById(request.getCategoryId())
            );
        }

        // Save and return response
        return vehicleMapper.toResponse(
                vehicleRepository.save(vehicle));
    }

    // Update existing vehicle
    @Transactional
    public VehicleResponse updateVehicle(Long id, VehicleRequest request) {

        // Fetch existing vehicle
        Vehicle existing = vehicleRepository.findById(id)
                .orElseThrow(() ->
                        new ResourceNotFoundException("Vehicle not found"));

        String newPlate = request.getRegistrationNumber().trim();


        if (!existing.getRegistrationNumber().equalsIgnoreCase(newPlate)) {
            if (vehicleRepository.existsByRegistrationNumberIgnoreCase(newPlate)) {
                throw new BadRequestException("A vehicle with registration number " + newPlate + " already exists.");
            }
            existing.setRegistrationNumber(newPlate.toUpperCase());
        }

        // Update fields
        existing.setName(request.getName().trim());
        existing.setType(request.getType());
        existing.setPricePerDay(request.getPricePerDay());
        existing.setDescription(request.getDescription());

        // Update category if provided
        if (request.getCategoryId() != null) {
            existing.setCategory(
                    categoryService.getCategoryById(request.getCategoryId())
            );
        }

        // Save updated data
        return vehicleMapper.toResponse(
                vehicleRepository.save(existing));
    }

    // Soft delete (mark inactive instead of removing)
    @Transactional
    public void softDeleteVehicle(Long id) {

        // Fetch vehicle
        Vehicle vehicle = vehicleRepository.findById(id)
                .orElseThrow(() ->
                        new ResourceNotFoundException("Vehicle not found"));

        // Block delete if active/pending bookings exist
        boolean hasActiveBookings = bookingRepository
                .existsByVehicleIdAndStatusIn(
                        id,
                        List.of(BookingStatus.ACTIVE, BookingStatus.PENDING)
                );

        if (hasActiveBookings) {
            throw new BadRequestException("Vehicle has active bookings");
        }

        vehicle.setActive(false); // Mark inactive
        vehicleRepository.save(vehicle);
    }

    // Toggle active/inactive status
    @Transactional
    public VehicleResponse toggleVehicleStatus(Long id) {

        // Fetch vehicle
        Vehicle vehicle = vehicleRepository.findById(id)
                .orElseThrow(() ->
                        new ResourceNotFoundException("Vehicle not found"));

        // If disabling, ensure no future bookings
        if (vehicle.isActive()) {
            boolean hasBookings = bookingRepository
                    .existsActiveOrFutureBookingsForVehicle(id);

            if (hasBookings) {
                throw new BadRequestException(
                        "Cannot deactivate: future bookings exist");
            }
        }

        vehicle.setActive(!vehicle.isActive()); // Flip status

        return vehicleMapper.toResponse(
                vehicleRepository.save(vehicle));
    }

    // Search for available vehicles by date range
    public List<VehicleResponse> findAvailableVehicles(LocalDate startDate, LocalDate endDate) {


        List<Vehicle> allVehicles = vehicleRepository.findAll();


        return allVehicles.stream()
                .filter(Vehicle::isActive)
                .filter(vehicle -> bookingRepository.isVehicleAvailable(vehicle.getId(), startDate, endDate))
                .map(vehicleMapper::toResponse)
                .toList();
    }
}

