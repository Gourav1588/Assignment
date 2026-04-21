package com.vehicle.rental.entity;

import com.fasterxml.jackson.annotation.JsonIgnore;
import jakarta.persistence.*;
import lombok.Data;
import java.util.List;

// I added this 4th entity to normalize the database. Instead of hardcoding
// "SUV" or "Sedan" as simple text strings in the Vehicle table, having a dedicated
// Category table lets the Admin dynamically add new vehicle types from the UI
// without us needing to rewrite the core code.
@Data
@Entity
@Table(name = "vehicle_categories")
public class VehicleCategory {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // I made the category name strictly unique because it acts as the primary filter
    // on the frontend. We don't want the Admin accidentally creating two separate
    // "Luxury" categories and confusing the users.
    @Column(nullable = false, unique = true)
    private String name;

    // Just a simple optional field to give users a bit more context
    // (e.g., "7-seaters perfect for family road trips").
    private String description;


    // 1. I used @JsonIgnore to prevent a catastrophic infinite recursion bug
    //    (where Category serializes Vehicle, Vehicle serializes Category, repeating
    //    until the server crashes with a StackOverflowError).
    // 2. I explicitly set FetchType.LAZY so that when we just want to load a simple
    //    list of category names for a dropdown menu, Hibernate doesn't secretly
    //    run massive SQL queries to load hundreds of associated vehicles into memory.
    @JsonIgnore
    @OneToMany(mappedBy = "category", fetch = FetchType.LAZY)
    private List<Vehicle> vehicles;
}