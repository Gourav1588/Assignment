package com.vehicle.rental.entity;

import jakarta.persistence.*;
import lombok.Data;
import java.time.LocalDateTime;

/**
 * JPA Entity representing a vehicle in the rental fleet.
 * Utilizes soft-deletion (isActive flag) to preserve historical booking records
 * while dynamically managing catalog availability.
 */
@Data
@Entity
@Table(name = "vehicles")
public class Vehicle {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    /**
     * The category classification of the vehicle.
     * Mapped as a foreign key to normalize the database and prevent duplicate text strings.
     */
    @ManyToOne
    @JoinColumn(name = "category_id")
    private VehicleCategory category;

    @Column(nullable = false)
    private String name;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private VehicleType type;

    /**
     * Unique legal identifier for the vehicle.
     */
    @Column(name = "registration_number", unique = true, nullable = false)
    private String registrationNumber;

    /**
     * Soft-delete flag. Instead of physically deleting retired cars (which would sever
     * historical booking foreign keys), this flag removes them from active user queries.
     */
    @Column(nullable = false)
    private boolean isActive = true;

    private String description;

    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt = LocalDateTime.now();

    /**
     * The current baseline daily rental rate for this specific vehicle.
     */
    @Column(name = "price_per_day", nullable = false)
    private Double pricePerDay;

    public enum VehicleType {
        CAR, BIKE
    }
}