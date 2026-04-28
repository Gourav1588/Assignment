package com.vehicle.rental.dto.response;

import com.vehicle.rental.entity.Vehicle.VehicleType;
import lombok.Data;

/**
 * Data Transfer Object representing vehicle details.
 * Sent to the client in response to catalog queries, abstracting away
 * internal database models and exposing only safe, relevant information.
 */
@Data
public class VehicleResponse {

    /**
     * The unique database identifier of the vehicle.
     */
    private Long id;

    /**
     * The display name or model of the vehicle (e.g., "Toyota Camry").
     */
    private String name;

    /**
     * The unique license plate or registration number of the vehicle.
     */
    private String registrationNumber;

    /**
     * The overarching classification type of the vehicle (e.g., CAR, BIKE).
     */
    private VehicleType type;

    /**
     * Additional details providing context about the vehicle's features or condition.
     */
    private String description;

    /**
     * The current daily rental rate for the vehicle.
     */
    private Double pricePerDay;

    /**
     * The display name of the category this vehicle belongs to (if assigned).
     */
    private String categoryName;

    /**
     * Flag indicating whether the vehicle is currently active in the system
     * (e.g., true if it is operational and part of the fleet, false if it is retired or suspended).
     */
    private boolean isActive;
}