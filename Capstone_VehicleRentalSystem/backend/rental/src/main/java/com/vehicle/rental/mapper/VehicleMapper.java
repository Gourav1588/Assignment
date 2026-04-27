package com.vehicle.rental.mapper;

import com.vehicle.rental.dto.request.VehicleRequest;
import com.vehicle.rental.dto.response.VehicleResponse;
import com.vehicle.rental.entity.Vehicle;
import org.springframework.stereotype.Component;

@Component // Marks as Spring component
public class VehicleMapper {

    // Convert request DTO → entity
    public Vehicle toEntity(VehicleRequest request) {

        Vehicle vehicle = new Vehicle(); // Create entity

        vehicle.setName(request.getName().trim()); // Set name
        vehicle.setType(request.getType()); // Set type
        vehicle.setPricePerDay(request.getPricePerDay()); // Set price
        vehicle.setDescription(request.getDescription()); // Set description

        vehicle.setActive(true); // Default active

        return vehicle; // Return entity
    }

    // Convert entity → response DTO
    public VehicleResponse toResponse(Vehicle vehicle) {

        VehicleResponse response = new VehicleResponse(); // Create DTO

        response.setId(vehicle.getId()); // Set id
        response.setName(vehicle.getName()); // Set name
        response.setType(vehicle.getType()); // Set type
        response.setDescription(vehicle.getDescription()); // Set description
        response.setPricePerDay(vehicle.getPricePerDay()); // Set price
        response.setActive(vehicle.isActive()); // Set status

        // Set category if exists
        if (vehicle.getCategory() != null) {
            response.setCategoryName(vehicle.getCategory().getName());
        }

        return response; // Return DTO
    }
}