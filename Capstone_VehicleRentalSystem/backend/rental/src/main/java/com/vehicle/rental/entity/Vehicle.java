package com.vehicle.rental.entity;

import com.fasterxml.jackson.annotation.JsonIgnore;
import jakarta.persistence.*;
import lombok.Data;
import java.time.LocalDateTime;


//  The @ManyToOne link to the Category table (preventing duplicate data).
//  The 'isActive' soft-delete flag. Instead of physically deleting retired cars
//    and destroying our historical booking records, we just toggle them off.
@Data
@Entity
@Table(name = "vehicles")
public class Vehicle {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;


    //  It saves a simple foreign key (category_id) instead of duplicating text strings.
    @ManyToOne
    @JoinColumn(name = "category_id")
    private VehicleCategory category;

    @Column(nullable = false)
    private String name;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private VehicleType type;

    // The Soft Delete.

    @Column(nullable = false)
    private boolean isActive = true;

    private String description;

    @Column(name = "created_at")
    private LocalDateTime createdAt = LocalDateTime.now();

    // The current daily rental rate for this specific vehicle.
    @Column(name = "price_per_day", nullable = false)
    private Double pricePerDay;

    public enum VehicleType {
        CAR, BIKE
    }
}