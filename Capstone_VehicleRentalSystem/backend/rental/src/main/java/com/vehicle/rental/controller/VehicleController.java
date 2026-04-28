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

@Slf4j // Enables logging
@RestController // Marks class as REST API controller
@RequestMapping("/api/vehicles") // Base URL mapping
@CrossOrigin(origins = "*") // Allows cross-origin requests
@RequiredArgsConstructor // Generates constructor for final fields
public class VehicleController {

    private final VehicleService vehicleService; // Service dependency

    // Fetch vehicles with optional filters and pagination
    @GetMapping
    public ResponseEntity<Page<VehicleResponse>> getVehicles(
            @RequestParam(defaultValue = "0") int page,       // Page number
            @RequestParam(defaultValue = "10") int size,      // Page size
            @RequestParam(required = false) VehicleType type,// Filter by type
            @RequestParam(required = false) Long categoryId, // Filter by category
            @RequestParam(required = false) String name) {   // Filter by name

        // Call service and return paginated response
        return ResponseEntity.ok(
                vehicleService.getVehicles(page, size, type, categoryId, name)
        );
    }


    @GetMapping("/search")
    public ResponseEntity<List<VehicleResponse>> searchAvailableVehicles(
            @RequestParam LocalDate startDate,
            @RequestParam LocalDate endDate) {

        log.info("Searching for vehicles between {} and {}", startDate, endDate);
        return ResponseEntity.ok(vehicleService.findAvailableVehicles(startDate, endDate));
    }
    @GetMapping("/{id}")
    public ResponseEntity<VehicleResponse> getVehicleById(@PathVariable Long id) {
        log.info("Fetching vehicle id: {}", id);
        return ResponseEntity.ok(vehicleService.getVehicleById(id));
    }

    // Create new vehicle (Admin only)
    @PostMapping
    @PreAuthorize("hasRole('ADMIN')") // Restrict access to ADMIN
    public ResponseEntity<VehicleResponse> createVehicle(
            @Valid @RequestBody VehicleRequest request) { // Validate input
        log.info("Creating vehicle: {}", request.getName()); // Log action
        return ResponseEntity.ok(vehicleService.createVehicle(request));
    }


    // Update existing vehicle (Admin only)
    @PutMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')") // Restrict access to ADMIN
    public ResponseEntity<VehicleResponse> updateVehicle(
            @PathVariable Long id,
            @Valid @RequestBody VehicleRequest request) {
        log.info("Updating vehicle id: {}", id);
        return ResponseEntity.ok(vehicleService.updateVehicle(id, request));
    }

    // Toggle vehicle availability/status (Admin only)
    @PutMapping("/{id}/toggle-status")
    @PreAuthorize("hasRole('ADMIN')") // Restrict access to ADMIN
    public ResponseEntity<VehicleResponse> toggleVehicleStatus(@PathVariable Long id) {
        log.info("Toggling status for vehicle id: {}", id); // Log action
        return ResponseEntity.ok(vehicleService.toggleVehicleStatus(id));
    }



}