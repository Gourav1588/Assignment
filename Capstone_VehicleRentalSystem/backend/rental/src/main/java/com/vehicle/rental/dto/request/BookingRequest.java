package com.vehicle.rental.dto.request;

import jakarta.validation.constraints.FutureOrPresent;
import jakarta.validation.constraints.NotNull;
import lombok.Data;

import java.time.LocalDate;

/**
 * Data Transfer Object for handling vehicle booking requests.
 * Captures and validates the required parameters from the client to initiate a new rental.
 */
@Data
public class BookingRequest {

    /**
     * The unique identifier of the vehicle being requested.
     */
    @NotNull(message = "Vehicle ID is required")
    private Long vehicleId;

    /**
     * The requested start date for the rental period.
     * Ensures the user cannot book a vehicle for a date that has already passed.
     */
    @NotNull(message = "Start date is required")
    @FutureOrPresent(message = "Start date cannot be in the past")
    private LocalDate startDate;

    /**
     * The requested end date for the rental period.
     */
    @NotNull(message = "End date is required")
    @FutureOrPresent(message = "End date must be today or in the future")
    private LocalDate endDate;
}