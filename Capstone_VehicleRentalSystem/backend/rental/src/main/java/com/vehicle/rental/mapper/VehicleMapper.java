package com.vehicle.rental.mapper;

import com.vehicle.rental.dto.request.VehicleRequest;
import com.vehicle.rental.dto.response.VehicleResponse;
import com.vehicle.rental.entity.Vehicle;
import org.springframework.stereotype.Component;

@Component
public class VehicleMapper {

    // Convert VehicleRequest DTO to Vehicle entity
    // Used while creating a new vehicle from client input
    public Vehicle toEntity(VehicleRequest request) {

        // Create new entity object
        Vehicle vehicle = new Vehicle();

        // Map basic fields from request to entity
        // Trim name to remove unnecessary spaces
        vehicle.setName(request.getName().trim());
        vehicle.setType(request.getType());
        vehicle.setPricePerDay(request.getPricePerDay());
        vehicle.setDescription(request.getDescription());

        // Set default status as active when creating a new vehicle
        vehicle.setActive(true);

        return vehicle;
    }

    // Convert Vehicle entity to VehicleResponse DTO
    // Used when sending data back to the client
    public VehicleResponse toResponse(Vehicle vehicle) {

        // Create response object
        VehicleResponse response = new VehicleResponse();

        // Map basic fields from entity to DTO
        response.setId(vehicle.getId());
        response.setName(vehicle.getName());
        response.setType(vehicle.getType());
        response.setDescription(vehicle.getDescription());
        response.setPricePerDay(vehicle.getPricePerDay());

        // Map category name if category exists
        // Prevents null pointer issues when category is not assigned
        if (vehicle.getCategory() != null) {
            response.setCategoryName(
                    vehicle.getCategory().getName()
            );
        }

        // Return mapped response object
        return response;
    }
}