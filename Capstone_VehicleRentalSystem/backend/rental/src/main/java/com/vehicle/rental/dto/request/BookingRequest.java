package com.vehicle.rental.dto.request;

import jakarta.validation.constraints.FutureOrPresent;
import jakarta.validation.constraints.NotNull;
import lombok.Data;

import java.time.LocalDateTime;

/**
 * Data Transfer Object for handling vehicle booking requests.
 * Captures and validates the required parameters from the client to initiate a new rental.
 * Upgraded to support exact-time scheduling.
 */
@Data
public class BookingRequest {

    /**
     * The unique identifier of the vehicle being requested.
     */
    @NotNull(message = "Vehicle ID is required")
    private Long vehicleId;

    /**
     * The requested start time (date and minute) for the rental period.
     * Ensures the user cannot book a vehicle for a time that has already passed.
     */
    @NotNull(message = "Start time is required")
    @FutureOrPresent(message = "Start time cannot be in the past")
    private LocalDateTime startTime;

    /**
     * The requested end time (date and minute) for the rental period.
     */
    @NotNull(message = "End time is required")
    @FutureOrPresent(message = "End time must be right now or in the future")
    private LocalDateTime endTime;
}