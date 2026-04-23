package com.vehicle.rental.dto.request;

import jakarta.validation.constraints.NotBlank;
import lombok.Data;

@Data
public class CategoryRequest {

    // Name of the category
    // Must not be blank to ensure valid input
    @NotBlank(message = "Category name is required")
    private String name;

    // Optional description to provide additional details about the category
    private String description;
}