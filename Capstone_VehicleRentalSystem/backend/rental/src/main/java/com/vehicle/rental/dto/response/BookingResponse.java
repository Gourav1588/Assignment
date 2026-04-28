package com.vehicle.rental.dto.response;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.vehicle.rental.entity.Booking.BookingStatus;
import lombok.Data;

import java.time.LocalDate;
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

    /**
     * The unique identifier of the booked vehicle.
     */
    private Long vehicleId;

    /**
     * The display name of the booked vehicle.
     */
    private String vehicleName;

    /**
     * The classification type of the vehicle (e.g., CAR, BIKE).
     */
    private String vehicleType;

    /**
     * The daily rental rate of the vehicle at the time of booking.
     */
    private Double pricePerDay;

    // --- Booking Details ---

    /**
     * The approved starting date of the rental period.
     */
    private LocalDate startDate;

    /**
     * The approved ending date of the rental period.
     */
    private LocalDate endDate;

    /**
     * The total number of days the vehicle is booked for.
     */
    private Long totalDays;

    /**
     * The calculated total cost of the booking (pricePerDay * totalDays).
     */
    private Double totalCost;

    /**
     * The current operational status of the booking (e.g., PENDING, ACTIVE, COMPLETED, CANCELLED).
     */
    private BookingStatus status;

    // --- User Details ---

    /**
     * The unique identifier of the user who made the booking.
     */
    private Long userId;

    /**
     * The name of the user who made the booking.
     */
    private String userName;

    /**
     * The exact timestamp when this booking record was created in the system.
     * Formatted as dd-MM-yyyy HH:mm:ss for standardized frontend display.
     */
    @JsonFormat(pattern = "dd-MM-yyyy HH:mm:ss")
    private LocalDateTime createdAt;
}