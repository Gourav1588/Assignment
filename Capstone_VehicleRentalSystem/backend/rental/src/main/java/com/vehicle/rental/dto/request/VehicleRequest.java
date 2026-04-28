package com.vehicle.rental.dto.request;

import com.vehicle.rental.entity.Vehicle.VehicleType;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import lombok.Data;

/**
 * Data Transfer Object for creating or updating vehicle records.
 * Captures and validates the necessary details required to add or modify a vehicle in the fleet.
 */
@Data
public class VehicleRequest {

    /**
     * The unique license plate or registration number of the vehicle.
     * This field is mandatory for legal identification and tracking purposes.
     */
    @NotBlank(message = "Registration number is required")
    private String registrationNumber;

    /**
     * The display name or model of the vehicle (e.g., "Toyota Camry", "Honda CR-V").
     * This field is mandatory and cannot be blank.
     */
    @NotBlank(message = "Vehicle name is required")
    private String name;

    /**
     * The overarching classification type of the vehicle (e.g., CAR, BIKE).
     * Required for high-level system categorization and search filtering.
     */
    @NotNull(message = "Vehicle type is required")
    private VehicleType type;

    /**
     * The base cost to rent this vehicle for a single day.
     * Must be a numerical value strictly greater than zero.
     */
    @NotNull(message = "Price per day is required")
    @Positive(message = "Price per day must be greater than 0")
    private Double pricePerDay;

    /**
     * An optional description providing additional details about the vehicle's features,
     * condition, or specific rental restrictions.
     */
    private String description;

    /**
     * The unique identifier of the specific category this vehicle belongs to (e.g., "Luxury", "Economy").
     * This is optional, allowing vehicles to exist outside of strict granular categories if needed.
     */
    private Long categoryId;
}