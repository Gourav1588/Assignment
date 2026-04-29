package com.vehicle.rental.entity;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import jakarta.persistence.*;
import lombok.Data;

import java.time.LocalDateTime;

/**
 * JPA Entity representing a vehicle rental booking transaction.
 * Connects a User to a specific Vehicle for a designated time period.
 * Designed as a dedicated entity rather than a simple join table to track
 * business-critical data like finalized pricing and lifecycle status.
 */
@Data
@Entity
@Table(name = "bookings")
public class Booking {

    /**
     * The unique primary key for the booking record.
     */
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    /**
     * The user who initiated the booking.
     * Sensitive and relational fields (password, role, and the user's other bookings)
     * are ignored during JSON serialization to ensure data security and prevent
     * infinite recursion (circular references).
     */
    @ManyToOne
    @JoinColumn(name = "user_id", nullable = false)
    @JsonIgnoreProperties({"bookings", "password", "role"})
    private User user;

    /**
     * The vehicle reserved for this booking.
     * Internal vehicle state flags and back-references are ignored during JSON serialization
     * to keep the API payload clean and focused on essential vehicle details.
     */
    @ManyToOne
    @JoinColumn(name = "vehicle_id", nullable = false)
    @JsonIgnoreProperties({"bookings", "isActive"})
    private Vehicle vehicle;

    /* =========================================================================
       TIME-BASED SCHEDULING UPGRADE
       ========================================================================= */

    /**
     * The exact approved start time (date and exact minute) of the rental period.
     * Upgraded to LocalDateTime to support granular, hourly bookings.
     */
    @Column(name = "start_time", nullable = false)
    private LocalDateTime startTime;

    /**
     * The exact approved end time (date and exact minute) of the rental period.
     * Upgraded to LocalDateTime to support same-day turnarounds and precise availability.
     */
    @Column(name = "end_time", nullable = false)
    private LocalDateTime endTime;

    /* ========================================================================= */

    /**
     * The finalized total cost of the booking.
     * This acts as a financial 'snapshot' at the exact moment of creation, ensuring historical
     * receipts remain accurate even if vehicle rental rates fluctuate in the future.
     */
    @Column(name = "total_cost", nullable = false)
    private Double totalCost;

    /**
     * The current lifecycle status of the transaction.
     * Defaults to PENDING, allowing the user to review the calculated financial summary
     * on the frontend before officially confirming the rental.
     */
    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private BookingStatus status = BookingStatus.PENDING;

    /**
     * The exact timestamp when this record was generated in the database.
     */
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt = LocalDateTime.now();

    /**
     * Enumeration of valid booking lifecycle states.
     * Supports a full historical audit trail for user dashboards and admin reporting.
     */
    public enum BookingStatus {
        /** Created but awaiting final user confirmation. */
        PENDING,
        /** Confirmed and currently within the active rental period. */
        ACTIVE,
        /** Terminated by the user prior to completion (retains the financial record). */
        CANCELLED,
        /** Trip finished successfully; the vehicle is returned and available for the next user. */
        COMPLETED
    }
}