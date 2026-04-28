package com.vehicle.rental.dto.response;

import lombok.Data;

/**
 * Data Transfer Object representing a vehicle category.
 * Used to safely transfer category details from the server to the client
 * without exposing internal database structures.
 */
@Data
public class CategoryResponse {

    /**
     * The unique identifier of the category.
     */
    private Long id;

    /**
     * The display name of the category (e.g., "SUV", "Luxury", "Economy").
     */
    private String name;

    /**
     * A brief description providing more context about the types of vehicles in this category.
     */
    private String description;
}