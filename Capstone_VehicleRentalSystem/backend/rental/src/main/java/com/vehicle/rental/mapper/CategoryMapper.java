package com.vehicle.rental.mapper;

import com.vehicle.rental.dto.request.CategoryRequest;
import com.vehicle.rental.dto.response.CategoryResponse;
import com.vehicle.rental.entity.VehicleCategory;
import org.springframework.stereotype.Component;

/**
 * Mapper component for translating between Category DTOs and internal Entities.
 */
@Component
public class CategoryMapper {

    /**
     * Converts an incoming CategoryRequest into a persistent VehicleCategory entity.
     *
     * @param request The data transfer object containing category input.
     * @return The populated VehicleCategory entity.
     */
    public VehicleCategory toEntity(CategoryRequest request) {
        VehicleCategory category = new VehicleCategory();
        category.setName(request.getName().trim());
        category.setDescription(request.getDescription());
        return category;
    }

    /**
     * Converts a VehicleCategory entity into a CategoryResponse DTO.
     *
     * @param category The source VehicleCategory entity.
     * @return The formatted CategoryResponse DTO.
     */
    public CategoryResponse toResponse(VehicleCategory category) {
        CategoryResponse response = new CategoryResponse();
        response.setId(category.getId());
        response.setName(category.getName());
        response.setDescription(category.getDescription());
        return response;
    }
}