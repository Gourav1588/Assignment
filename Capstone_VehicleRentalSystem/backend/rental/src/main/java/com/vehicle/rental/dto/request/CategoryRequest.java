package com.vehicle.rental.dto.request;

import jakarta.validation.constraints.NotBlank;
import lombok.Data;

/**
 * Data Transfer Object for creating or updating vehicle categories.
 */
@Data
public class CategoryRequest {

    /**
     * The display name of the category (e.g., "SUV", "Luxury", "Economy").
     * This field is mandatory and cannot consist of only whitespace.
     */
    @NotBlank(message = "Category name is required")
    private String name;

    /**
     * An optional description providing more context about the types of vehicles in this category.
     */
    private String description;
}