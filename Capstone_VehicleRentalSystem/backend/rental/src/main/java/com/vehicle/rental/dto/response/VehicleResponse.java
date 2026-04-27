package com.vehicle.rental.dto.response;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.vehicle.rental.entity.Vehicle.VehicleType;
import lombok.Data;

@Data
public class VehicleResponse {

    // Unique identifier of the vehicle
    private Long id;

    // Name of the vehicle
    private String name;

    // Type of the vehicle (e.g., CAR, BIKE)
    private VehicleType type;

    // Description providing additional details about the vehicle
    private String description;

    // Rental price per day
    private Double pricePerDay;

    // Name of the associated category (if any)
    private String categoryName;

    // Status flag
    private boolean isActive;


}