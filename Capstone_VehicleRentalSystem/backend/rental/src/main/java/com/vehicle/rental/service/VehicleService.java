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

/**
 * Service layer handling fleet inventory management.
 * Controls the creation, modification, and status toggling of vehicles, enforcing
 * strict uniqueness on registration plates and safeguarding active bookings.
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class VehicleService {

    private final VehicleRepository vehicleRepository;
    private final BookingRepository bookingRepository;
    private final CategoryService categoryService;
    private final VehicleMapper vehicleMapper;

    /**
     * Retrieves a paginated and filtered list of vehicles for the catalog.
     */
    public Page<VehicleResponse> getVehicles(int page, int size, VehicleType type, Long categoryId, String name) {
        if (page < 0) throw new BadRequestException("Pagination index cannot be negative");
        if (size <= 0) throw new BadRequestException("Pagination size must be strictly positive");

        Pageable pageable = PageRequest.of(page, size, Sort.by("createdAt").descending());

        return vehicleRepository
                .findAllWithFilters(name != null && !name.isBlank() ? name : "", type, categoryId, pageable)
                .map(vehicleMapper::toResponse);
    }

    public VehicleResponse getVehicleById(Long id) {
        Vehicle vehicle = vehicleRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Vehicle record not found"));
        return vehicleMapper.toResponse(vehicle);
    }

    /**
     * Integrates a new vehicle into the fleet.
     * Validates that the legal registration number is not already registered in the system.
     */
    @Transactional
    public VehicleResponse createVehicle(VehicleRequest request) {
        String normalizedName = request.getName().trim();
        String normalizedPlate = request.getRegistrationNumber().trim();

        if (vehicleRepository.existsByRegistrationNumberIgnoreCase(normalizedPlate)) {
            throw new BadRequestException("Registration number " + normalizedPlate + " already exists in the fleet.");
        }

        Vehicle vehicle = vehicleMapper.toEntity(request);
        vehicle.setName(normalizedName);

        if (request.getCategoryId() != null) {
            vehicle.setCategory(categoryService.getCategoryById(request.getCategoryId()));
        }

        log.info("Fleet expanded with new vehicle: {} [{}]", normalizedName, normalizedPlate);
        return vehicleMapper.toResponse(vehicleRepository.save(vehicle));
    }

    /**
     * Updates an existing vehicle's attributes.
     * Safely checks for registration number collisions if the plate is being modified.
     */
    @Transactional
    public VehicleResponse updateVehicle(Long id, VehicleRequest request) {
        Vehicle existing = vehicleRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Vehicle record not found"));

        String newPlate = request.getRegistrationNumber().trim();

        if (!existing.getRegistrationNumber().equalsIgnoreCase(newPlate)) {
            if (vehicleRepository.existsByRegistrationNumberIgnoreCase(newPlate)) {
                throw new BadRequestException("Registration number " + newPlate + " is mapped to another vehicle.");
            }
            existing.setRegistrationNumber(newPlate.toUpperCase());
        }

        existing.setName(request.getName().trim());
        existing.setType(request.getType());
        existing.setPricePerDay(request.getPricePerDay());
        existing.setDescription(request.getDescription());

        if (request.getCategoryId() != null) {
            existing.setCategory(categoryService.getCategoryById(request.getCategoryId()));
        }

        return vehicleMapper.toResponse(vehicleRepository.save(existing));
    }

    /**
     * Flips the operational status of a vehicle (Active <-> Inactive).
     * Acts as a soft-delete mechanism. Prevents deactivation if the vehicle is tied
     * to future or ongoing reservations to prevent system conflicts.
     */
    @Transactional
    public VehicleResponse toggleVehicleStatus(Long id) {
        Vehicle vehicle = vehicleRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Vehicle record not found"));

        if (vehicle.isActive()) {
            boolean hasBookings = bookingRepository.existsActiveOrFutureBookingsForVehicle(id);
            if (hasBookings) {
                throw new BadRequestException("Cannot deactivate vehicle: Future or active bookings exist.");
            }
        }

        vehicle.setActive(!vehicle.isActive());
        log.info("Vehicle ID {} status toggled to Active: {}", id, vehicle.isActive());

        return vehicleMapper.toResponse(vehicleRepository.save(vehicle));
    }

    public List<VehicleResponse> findAvailableVehicles(LocalDate startDate, LocalDate endDate) {
        List<Vehicle> allVehicles = vehicleRepository.findAll();

        return allVehicles.stream()
                .filter(Vehicle::isActive)
                .filter(vehicle -> bookingRepository.isVehicleAvailable(vehicle.getId(), startDate, endDate))
                .map(vehicleMapper::toResponse)
                .toList();
    }
}

