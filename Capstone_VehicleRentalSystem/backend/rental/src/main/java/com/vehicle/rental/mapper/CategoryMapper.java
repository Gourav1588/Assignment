package com.vehicle.rental.mapper;

import com.vehicle.rental.dto.request.CategoryRequest;
import com.vehicle.rental.dto.response.CategoryResponse;
import com.vehicle.rental.entity.VehicleCategory;
import org.springframework.stereotype.Component;

@Component
public class CategoryMapper {

    public VehicleCategory toEntity(CategoryRequest request) {
        VehicleCategory category = new VehicleCategory();
        category.setName(request.getName().trim());
        category.setDescription(request.getDescription());
        return category;
    }

    public CategoryResponse toResponse(VehicleCategory category) {
        CategoryResponse response = new CategoryResponse();
        response.setId(category.getId());
        response.setName(category.getName());
        response.setDescription(category.getDescription());
        return response;
    }
}