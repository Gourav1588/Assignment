package com.vehicle.rental.service;

import com.vehicle.rental.dto.request.CategoryRequest;
import com.vehicle.rental.dto.response.CategoryResponse;
import com.vehicle.rental.entity.VehicleCategory;
import com.vehicle.rental.exception.BadRequestException;
import com.vehicle.rental.exception.ResourceNotFoundException;
import com.vehicle.rental.mapper.CategoryMapper;
import com.vehicle.rental.repository.CategoryRepository;
import com.vehicle.rental.repository.VehicleRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Slf4j
@Service
@RequiredArgsConstructor
public class CategoryService {

    // Repository for category-related database operations
    private final CategoryRepository categoryRepository;

    // Repository used to validate category usage before deletion
    private final VehicleRepository vehicleRepository;

    // Mapper to convert between DTOs and entity
    private final CategoryMapper categoryMapper;

    // Fetch all categories
    // Converts entity list to response DTOs for client consumption
    public List<CategoryResponse> getAllCategories() {
        return categoryRepository.findAll()
                .stream()
                .map(categoryMapper::toResponse)
                .collect(Collectors.toList());
    }

    // Retrieve a category entity by ID
    // Used internally by other services (e.g., VehicleService)
    public VehicleCategory getCategoryById(Long id) {
        return categoryRepository.findById(id)
                .orElseThrow(() ->
                        new ResourceNotFoundException("Category not found"));
    }

    // Create a new category
    // Validates input, saves entity, and returns response DTO
    @Transactional
    public CategoryResponse createCategory(CategoryRequest request) {
        log.debug("Creating category: {}", request.getName());

        // Check for duplicate category name
        if (categoryRepository.existsByName(request.getName().trim())) {
            throw new BadRequestException(
                    "Category already exists: " + request.getName()
            );
        }

        // Convert request DTO to entity and save
        VehicleCategory savedCategory =
                categoryRepository.save(
                        categoryMapper.toEntity(request)
                );

        // Convert saved entity to response DTO
        return categoryMapper.toResponse(savedCategory);
    }

    // Update an existing category
    // Ensures category exists and validates duplicate names
    @Transactional
    public CategoryResponse updateCategory(Long id, CategoryRequest request) {
        log.debug("Updating category id: {}", id);

        // Fetch existing category or throw exception
        VehicleCategory existing = getCategoryById(id);

        // Validate duplicate name only if it has changed
        if (!existing.getName().equals(request.getName().trim()) &&
                categoryRepository.existsByName(request.getName().trim())) {
            throw new BadRequestException(
                    "Category name already exists: " + request.getName()
            );
        }

        // Update fields
        existing.setName(request.getName().trim());
        existing.setDescription(request.getDescription());

        // Save updated entity and convert to response DTO
        VehicleCategory updatedCategory =
                categoryRepository.save(existing);

        return categoryMapper.toResponse(updatedCategory);
    }

    // Delete a category safely
    // Ensures no vehicles are associated before deletion
    @Transactional
    public void deleteCategory(Long id) {
        log.debug("Deleting category id: {}", id);

        // Check if category exists
        if (!categoryRepository.existsById(id)) {
            throw new ResourceNotFoundException("Category not found");
        }

        // Prevent deletion if category is linked to any vehicle
        if (vehicleRepository.existsByCategoryId(id)) {
            throw new BadRequestException(
                    "Cannot delete category — it is assigned to existing vehicles"
            );
        }

        // Perform deletion
        categoryRepository.deleteById(id);

        log.debug("Category {} deleted successfully", id);
    }
}