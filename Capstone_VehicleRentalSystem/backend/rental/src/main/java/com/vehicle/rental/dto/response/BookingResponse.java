package com.vehicle.rental.dto.response;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.vehicle.rental.entity.Booking.BookingStatus;
import lombok.Data;

import java.time.LocalDateTime;

/**
 * Data Transfer Object representing a vehicle booking.
 * Contains comprehensive details about the transaction, including vehicle info,
 * rental duration, cost breakdown, and user details, formatted for client consumption.
 */
@Data
public class BookingResponse {

    /**
     * The unique identifier of the booking record.
     */
    private Long id;

    // --- Vehicle Details ---

    private Long vehicleId;
    private String vehicleName;
    private String vehicleType;
    private Double pricePerDay;

    // --- Booking Details ---

    /**
     * The approved starting time of the rental period.
     * Formatted for direct frontend display without timezone parsing issues.
     */
    @JsonFormat(pattern = "dd-MM-yyyy HH:mm")
    private LocalDateTime startTime;

    /**
     * The approved ending time of the rental period.
     * Formatted for direct frontend display.
     */
    @JsonFormat(pattern = "dd-MM-yyyy HH:mm")
    private LocalDateTime endTime;

    /**
     * The total number of hours the vehicle is booked for.
     * Replaces 'totalDays' to support granular, time-based billing.
     */
    private Long totalHours;

    /**
     * The calculated total cost of the booking.
     */
    private Double totalCost;

    /**
     * The current operational status of the booking.
     */
    private BookingStatus status;

    // --- User Details ---

    private Long userId;
    private String userName;

    /**
     * The exact timestamp when this booking record was created in the system.
     * Formatted as dd-MM-yyyy HH:mm:ss for standardized frontend display.
     */
    @JsonFormat(pattern = "dd-MM-yyyy HH:mm:ss")
    private LocalDateTime createdAt;
}