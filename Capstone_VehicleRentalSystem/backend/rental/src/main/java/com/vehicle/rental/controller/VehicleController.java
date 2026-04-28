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

/* =========================================================================
   VEHICLE CONTROLLER
   REST API endpoints for the vehicle catalog. Routes traffic between public
   browsing requests and secure, admin-level fleet management operations.
   ========================================================================= */
@Slf4j
@RestController
@RequestMapping("/api/vehicles")
@RequiredArgsConstructor
public class VehicleController {

    private final VehicleService vehicleService;

    /* =========================================================================
       1. PUBLIC READ ENDPOINTS (RESTRICTED DATA)
       ========================================================================= */

    /**
     * [DOOR 1: PUBLIC CATALOG]
     * Retrieves a paginated list of vehicles.
     * Passes 'false' for isAdmin to ensure users only see operational inventory.
     */
    @GetMapping
    public ResponseEntity<Page<VehicleResponse>> getPublicVehicles(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(required = false) VehicleType type,
            @RequestParam(required = false) Long categoryId,
            @RequestParam(required = false) String name) {

        log.info("Public fetch vehicles - Page: {}, Size: {}, Type: {}, CategoryId: {}, Name: {}",
                page, size, type, categoryId, name);

        // isAdmin flag set to false
        return ResponseEntity.ok(vehicleService.getVehicles(page, size, type, categoryId, name, false));
    }

    /**
     * Searches for available vehicles based on a specific date range.
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
     */
    @GetMapping("/{id}")
    public ResponseEntity<VehicleResponse> getVehicleById(@PathVariable Long id) {
        log.info("Fetching details for vehicle ID: {}", id);
        return ResponseEntity.ok(vehicleService.getVehicleById(id));
    }

    /* =========================================================================
       2. SECURE ADMIN ENDPOINTS (UNRESTRICTED DATA)
       ========================================================================= */

    /**
     * [DOOR 2: ADMIN DASHBOARD]
     * Retrieves a paginated list of the entire fleet (Active + Retired).
     * Protected by PreAuthorize to ensure only authorized administrators can access.
     */
    @GetMapping("/admin")
    @PreAuthorize("hasAuthority('ADMIN')")
    public ResponseEntity<Page<VehicleResponse>> getAdminVehicles(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(required = false) VehicleType type,
            @RequestParam(required = false) Long categoryId,
            @RequestParam(required = false) String name) {

        log.info("Admin fetch full fleet - Page: {}, Size: {}, Type: {}, CategoryId: {}, Name: {}",
                page, size, type, categoryId, name);

        // isAdmin flag set to true
        return ResponseEntity.ok(vehicleService.getVehicles(page, size, type, categoryId, name, true));
    }

    /* =========================================================================
       3. SECURE MUTATION ENDPOINTS (WRITE OPERATIONS)
       ========================================================================= */

    /**
     * Adds a new vehicle to the fleet.
     */
    @PostMapping
    @PreAuthorize("hasAuthority('ADMIN')")
    public ResponseEntity<VehicleResponse> createVehicle(@Valid @RequestBody VehicleRequest request) {
        log.info("Admin request to create new vehicle: {}", request.getName());
        return ResponseEntity.ok(vehicleService.createVehicle(request));
    }

    /**
     * Updates an existing vehicle's information.
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
     * Acts as a soft-delete (Retire/Activate).
     */
    @PutMapping("/{id}/toggle-status")
    @PreAuthorize("hasAuthority('ADMIN')")
    public ResponseEntity<VehicleResponse> toggleVehicleStatus(@PathVariable Long id) {
        log.info("Admin request to toggle status for vehicle ID: {}", id);
        return ResponseEntity.ok(vehicleService.toggleVehicleStatus(id));
    }
}