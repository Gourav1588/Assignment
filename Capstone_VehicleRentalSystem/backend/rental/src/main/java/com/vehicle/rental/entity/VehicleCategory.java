package com.vehicle.rental.entity;

import com.fasterxml.jackson.annotation.JsonIgnore;
import jakarta.persistence.*;
import lombok.Data;
import java.util.List;

/**
 * JPA Entity representing a dynamic vehicle classification.
 * Normalizes the database to allow administrators to configure new vehicle types
 * without modifying core application code.
 */
@Data
@Entity
@Table(name = "vehicle_categories")
public class VehicleCategory {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    /**
     * The display name of the category.
     * Enforced as strictly unique to prevent administrative duplication and UI confusion.
     */
    @Column(nullable = false, unique = true)
    private String name;

    /**
     * Optional contextual information regarding the category's intended use case.
     */
    private String description;

    /**
     * The collection of vehicles belonging to this category.
     * Annotated with @JsonIgnore to prevent infinite recursion during serialization.
     * Configured with FetchType.LAZY to prevent massive N+1 query memory loads
     * when simply fetching category names for frontend dropdowns.
     */
    @JsonIgnore
    @OneToMany(mappedBy = "category", fetch = FetchType.LAZY)
    private List<Vehicle> vehicles;
}