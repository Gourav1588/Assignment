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

@Slf4j
@RestController
@RequestMapping("/api/vehicles")
@CrossOrigin(origins = "*")
@RequiredArgsConstructor
public class VehicleController {

    private final VehicleService vehicleService;

    // Public: Anyone can see and search the fleet
    @GetMapping
    public ResponseEntity<Page<VehicleResponse>> getVehicles(
            @RequestParam(defaultValue = "0")   int page,
            @RequestParam(defaultValue = "10")  int size,
            @RequestParam(required = false)     VehicleType type,
            @RequestParam(required = false)     Long categoryId,
            @RequestParam(required = false)     String name) {

        // Notice we don't need the mapper here anymore,
        // because your Service already returns Page<VehicleResponse>!
        return ResponseEntity.ok(
                vehicleService.getVehicles(page, size, type, categoryId, name)
        );
    }

    // Public: Get details for a single vehicle
    @GetMapping("/{id}")
    public ResponseEntity<VehicleResponse> getVehicleById(@PathVariable Long id) {
        return ResponseEntity.ok(vehicleService.getVehicleById(id));
    }

    // Admin Only: Create a new car using VehicleRequest DTO
    @PostMapping
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<VehicleResponse> createVehicle(
            @Valid @RequestBody VehicleRequest request) {
        log.info("Admin creating new vehicle: {}", request.getName());
        return ResponseEntity.ok(vehicleService.createVehicle(request));
    }

    // Admin Only: Edit car details using VehicleRequest DTO
    @PutMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<VehicleResponse> updateVehicle(
            @PathVariable Long id,
            @Valid @RequestBody VehicleRequest request) {
        return ResponseEntity.ok(vehicleService.updateVehicle(id, request));
    }

    // Admin Only: Deactivate car (Soft Delete)
    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<ApiResponse> softDeleteVehicle(@PathVariable Long id) {
        vehicleService.softDeleteVehicle(id);

        // Uses your ApiResponse with the AllArgsConstructor
        return ResponseEntity.ok(new ApiResponse("Vehicle deactivated successfully", true));
    }
}