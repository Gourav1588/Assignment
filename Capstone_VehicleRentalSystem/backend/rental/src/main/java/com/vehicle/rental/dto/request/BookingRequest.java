package com.vehicle.rental.dto.request;

import jakarta.validation.constraints.Future;
import jakarta.validation.constraints.FutureOrPresent;
import jakarta.validation.constraints.NotNull;
import lombok.Data;

import java.time.LocalDate;

@Data
public class BookingRequest {

    // ID of the vehicle to be booked
    // Required field to identify which vehicle is selected
    @NotNull(message = "Vehicle ID is required")
    private Long vehicleId;

    // Start date of the booking
    // Must be provided and should be a future date
    @NotNull(message = "Start date is required")
    @FutureOrPresent(message = "Start date cannot be in the past")
    private LocalDate startDate;

    // End date of the booking
    // Must be provided and should also be a future date
    @NotNull(message = "End date is required")
    @Future(message = "End date must be in the future")
    private LocalDate endDate;
}