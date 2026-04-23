package com.vehicle.rental.dto.request;

import com.vehicle.rental.entity.Vehicle.VehicleType;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import lombok.Data;

@Data
public class VehicleRequest {

    // Name of the vehicle
    // Must not be blank to ensure valid input
    @NotBlank(message = "Vehicle name is required")
    private String name;

    // Type of the vehicle (e.g., CAR, BIKE)
    // Required field for classification
    @NotNull(message = "Vehicle type is required")
    private VehicleType type;

    // Rental price per day
    // Must be provided and greater than zero
    @NotNull(message = "Price per day is required")
    @Positive(message = "Price per day must be greater than 0")
    private Double pricePerDay;

    // Optional description for additional details about the vehicle
    private String description;

    // Optional category reference
    // Vehicle may or may not belong to a category
    private Long categoryId;
}