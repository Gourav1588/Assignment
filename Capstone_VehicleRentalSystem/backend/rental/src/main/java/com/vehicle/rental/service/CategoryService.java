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

    private final CategoryRepository categoryRepository;
    private final VehicleRepository vehicleRepository;
    private final CategoryMapper categoryMapper;

    public List<CategoryResponse> getAllCategories() {
        return categoryRepository.findAll()
                .stream()
                .map(categoryMapper::toResponse)
                .collect(Collectors.toList());
    }

    public VehicleCategory getCategoryById(Long id) {
        return categoryRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Category not found"));
    }

    @Transactional
    public CategoryResponse createCategory(CategoryRequest request) {
        String normalizedName = request.getName().trim();
        log.debug("Processing category: {}", normalizedName);

        // Find existing or Create new to prevent Duplicate Name crashes
        return categoryRepository.findByNameIgnoreCase(normalizedName)
                .map(categoryMapper::toResponse)
                .orElseGet(() -> {
                    VehicleCategory newCategory = categoryMapper.toEntity(request);
                    return categoryMapper.toResponse(categoryRepository.save(newCategory));
                });
    }

    @Transactional
    public CategoryResponse updateCategory(Long id, CategoryRequest request) {
        VehicleCategory existing = getCategoryById(id);
        String newName = request.getName().trim();

        if (!existing.getName().equalsIgnoreCase(newName) &&
                categoryRepository.existsByName(newName)) {
            throw new BadRequestException("Category name already exists: " + newName);
        }

        existing.setName(newName);
        existing.setDescription(request.getDescription());
        return categoryMapper.toResponse(categoryRepository.save(existing));
    }

}