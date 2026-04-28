package com.vehicle.rental.mapper;

import com.vehicle.rental.dto.request.VehicleRequest;
import com.vehicle.rental.dto.response.VehicleResponse;
import com.vehicle.rental.entity.Vehicle;
import org.springframework.stereotype.Component;

/**
 * Mapper component for translating between Vehicle DTOs and internal Entities.
 */
@Component
public class VehicleMapper {

    /**
     * Converts an incoming VehicleRequest DTO into a persistent Vehicle entity.
     * Ensures critical strings like registration numbers are trimmed and standardized.
     *
     * @param request The data transfer object containing vehicle input.
     * @return The populated Vehicle entity.
     */
    public Vehicle toEntity(VehicleRequest request) {
        Vehicle vehicle = new Vehicle();

        if (request.getRegistrationNumber() != null) {
            vehicle.setRegistrationNumber(request.getRegistrationNumber().trim().toUpperCase());
        }

        vehicle.setName(request.getName().trim());
        vehicle.setType(request.getType());
        vehicle.setPricePerDay(request.getPricePerDay());
        vehicle.setDescription(request.getDescription());

        // Defaults to true upon creation
        vehicle.setActive(true);

        return vehicle;
    }

    /**
     * Converts a Vehicle entity into a flat VehicleResponse DTO.
     * Safely extracts related category names without exposing full nested objects.
     *
     * @param vehicle The source Vehicle entity.
     * @return The formatted VehicleResponse DTO.
     */
    public VehicleResponse toResponse(Vehicle vehicle) {
        VehicleResponse response = new VehicleResponse();

        response.setId(vehicle.getId());
        response.setRegistrationNumber(vehicle.getRegistrationNumber());
        response.setName(vehicle.getName());
        response.setType(vehicle.getType());
        response.setDescription(vehicle.getDescription());
        response.setPricePerDay(vehicle.getPricePerDay());
        response.setActive(vehicle.isActive());

        if (vehicle.getCategory() != null) {
            response.setCategoryName(vehicle.getCategory().getName());
        }

        return response;
    }
}