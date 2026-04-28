package com.vehicle.rental.controller;

import com.vehicle.rental.dto.request.VehicleRequest;
import com.vehicle.rental.dto.response.ApiResponse;
import com.vehicle.rental.dto.response.VehicleResponse;
import com.vehicle.rental.entity.Vehicle.VehicleType;
import com.vehicle.rental.service.VehicleService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;
import java.util.List;

/**
 * REST Controller managing the vehicle catalog.
 * Provides public endpoints for searching/filtering vehicles and secured endpoints for fleet management.
 */
@Slf4j
@RestController
@RequestMapping("/api/vehicles")
@RequiredArgsConstructor
public class VehicleController {

    private final VehicleService vehicleService;

    /**
     * Retrieves a paginated list of vehicles with optional filtering.
     * This is a public endpoint used for browsing the catalog.
     *
     * @param page       The page number to retrieve (0-based indexing).
     * @param size       The number of records per page.
     * @param type       (Optional) Filter by vehicle type.
     * @param categoryId (Optional) Filter by specific category ID.
     * @param name       (Optional) Filter by vehicle name.
     * @return A paginated list of VehicleResponse objects.
     */
    @GetMapping
    public ResponseEntity<Page<VehicleResponse>> getVehicles(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(required = false) VehicleType type,
            @RequestParam(required = false) Long categoryId,
            @RequestParam(required = false) String name) {

        log.info("Fetching vehicles - Page: {}, Size: {}, Type: {}, CategoryId: {}, Name: {}",
                page, size, type, categoryId, name);

        return ResponseEntity.ok(vehicleService.getVehicles(page, size, type, categoryId, name));
    }

    /**
     * Searches for available vehicles based on a specific date range.
     * This is a public endpoint used during the booking flow.
     *
     * @param startDate The requested rental start date.
     * @param endDate   The requested rental end date.
     * @return A list of available VehicleResponse objects.
     */
    @GetMapping("/search")
    public ResponseEntity<List<VehicleResponse>> searchAvailableVehicles(
            @RequestParam LocalDate startDate,
            @RequestParam LocalDate endDate) {

        log.info("Searching for available vehicles between {} and {}", startDate, endDate);

        return ResponseEntity.ok(vehicleService.findAvailableVehicles(startDate, endDate));
    }

    /**
     * Retrieves the details of a specific vehicle by its ID.
     *
     * @param id The unique identifier of the vehicle.
     * @return The requested VehicleResponse object.
     */
    @GetMapping("/{id}")
    public ResponseEntity<VehicleResponse> getVehicleById(@PathVariable Long id) {

        log.info("Fetching details for vehicle ID: {}", id);

        return ResponseEntity.ok(vehicleService.getVehicleById(id));
    }

    /**
     * Adds a new vehicle to the fleet.
     * Restricted to users with the ADMIN authority.
     *
     * @param request The validated payload containing the vehicle details.
     * @return The created VehicleResponse object.
     */
    @PostMapping
    @PreAuthorize("hasAuthority('ADMIN')")
    public ResponseEntity<VehicleResponse> createVehicle(@Valid @RequestBody VehicleRequest request) {

        log.info("Admin request to create new vehicle: {}", request.getName());

        return ResponseEntity.ok(vehicleService.createVehicle(request));
    }

    /**
     * Updates an existing vehicle's information.
     * Restricted to users with the ADMIN authority.
     *
     * @param id      The unique identifier of the vehicle to update.
     * @param request The validated payload containing the updated details.
     * @return The updated VehicleResponse object.
     */
    @PutMapping("/{id}")
    @PreAuthorize("hasAuthority('ADMIN')")
    public ResponseEntity<VehicleResponse> updateVehicle(
            @PathVariable Long id,
            @Valid @RequestBody VehicleRequest request) {

        log.info("Admin request to update vehicle ID: {}", id);

        return ResponseEntity.ok(vehicleService.updateVehicle(id, request));
    }

    /**
     * Toggles the operational status (availability) of a vehicle.
     * Restricted to users with the ADMIN authority.
     *
     * @param id The unique identifier of the vehicle.
     * @return The updated VehicleResponse object.
     */
    @PutMapping("/{id}/toggle-status")
    @PreAuthorize("hasAuthority('ADMIN')")
    public ResponseEntity<VehicleResponse> toggleVehicleStatus(@PathVariable Long id) {

        log.info("Admin request to toggle status for vehicle ID: {}", id);

        return ResponseEntity.ok(vehicleService.toggleVehicleStatus(id));
    }
}