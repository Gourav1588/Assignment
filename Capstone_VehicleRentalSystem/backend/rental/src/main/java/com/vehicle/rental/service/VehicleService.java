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
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Slf4j
@Service
@RequiredArgsConstructor
public class VehicleService {

    // Repository for vehicle-related database operations
    private final VehicleRepository vehicleRepository;

    // Repository used to validate booking constraints
    private final BookingRepository bookingRepository;

    // Service used to fetch category details
    private final CategoryService categoryService;

    // Mapper to convert between Entity and DTO
    private final VehicleMapper vehicleMapper;

    // Fetch all active vehicles with pagination and optional filters
    // Supports filtering by type, category, and name (search)
    public Page<VehicleResponse> getVehicles(
            int page, int size,
            VehicleType type,
            Long categoryId,
            String name) {

        // Validate pagination inputs
        if (page < 0) {
            throw new BadRequestException(
                    "Page number cannot be negative");
        }

        if (size <= 0) {
            throw new BadRequestException(
                    "Page size must be greater than 0");
        }

        // Create pageable object with sorting (latest first)
        Pageable pageable = PageRequest.of(
                page, size, Sort.by("createdAt").descending()
        );

        // Call repository with dynamic filters
        // Null values are ignored in query automatically
        return vehicleRepository
                .findAllWithFilters(
                        name != null && !name.isBlank() ? name : null,
                        type,
                        categoryId,
                        pageable
                )
                // Convert entity to response DTO
                .map(vehicleMapper::toResponse);
    }

    // Retrieve a single vehicle by its ID
    // Used when viewing detailed vehicle information
    public VehicleResponse getVehicleById(Long id) {
        Vehicle vehicle = vehicleRepository.findById(id)
                .orElseThrow(() ->
                        new ResourceNotFoundException("Vehicle not found"));

        return vehicleMapper.toResponse(vehicle);
    }

    // Create a new vehicle
    @Transactional
    public VehicleResponse createVehicle(VehicleRequest request) {
        log.debug("Creating vehicle: {}", request.getName());

        // Convert request DTO to entity
        Vehicle vehicle = vehicleMapper.toEntity(request);

        // Assign category if provided
        if (request.getCategoryId() != null) {
            vehicle.setCategory(
                    categoryService.getCategoryById(
                            request.getCategoryId())
            );
        }

        // Save entity and return response DTO
        return vehicleMapper.toResponse(
                vehicleRepository.save(vehicle));
    }

    // Update an existing vehicle
    @Transactional
    public VehicleResponse updateVehicle(
            Long id, VehicleRequest request) {
        log.debug("Updating vehicle id: {}", id);

        // Fetch existing vehicle or throw exception
        Vehicle existing = vehicleRepository.findById(id)
                .orElseThrow(() ->
                        new ResourceNotFoundException("Vehicle not found"));

        // Update basic fields
        existing.setName(request.getName().trim());
        existing.setType(request.getType());
        existing.setPricePerDay(request.getPricePerDay());
        existing.setDescription(request.getDescription());

        // Update category if provided
        if (request.getCategoryId() != null) {
            existing.setCategory(
                    categoryService.getCategoryById(
                            request.getCategoryId())
            );
        }

        // Save updated entity and return response
        return vehicleMapper.toResponse(
                vehicleRepository.save(existing));
    }

    // Soft delete vehicle (mark as inactive)
    // Prevents data loss and keeps booking history intact
    @Transactional
    public void softDeleteVehicle(Long id) {
        log.debug("Soft deleting vehicle id: {}", id);

        // Fetch vehicle or throw exception
        Vehicle vehicle = vehicleRepository.findById(id)
                .orElseThrow(() ->
                        new ResourceNotFoundException("Vehicle not found"));

        // Check if vehicle has active or pending bookings
        boolean hasActiveBookings = bookingRepository
                .existsByVehicleIdAndStatusIn(
                        id,
                        List.of(BookingStatus.ACTIVE, BookingStatus.PENDING)
                );

        // Prevent deletion if bookings exist
        if (hasActiveBookings) {
            throw new BadRequestException(
                    "Cannot deactivate vehicle — " +
                            "it has active or pending bookings"
            );
        }

        // Mark vehicle as inactive (soft delete)
        vehicle.setActive(false);
        vehicleRepository.save(vehicle);

        log.debug("Vehicle {} soft deleted successfully", id);
    }
}