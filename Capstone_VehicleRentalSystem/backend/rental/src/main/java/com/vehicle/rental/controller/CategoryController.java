package com.vehicle.rental.controller;

import com.vehicle.rental.dto.request.CategoryRequest;
import com.vehicle.rental.dto.response.ApiResponse;
import com.vehicle.rental.dto.response.CategoryResponse;
import com.vehicle.rental.service.CategoryService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * REST Controller managing vehicle categories.
 * Provides public endpoints for viewing categories and secured endpoints for administrative management.
 */
@Slf4j
@RestController
@RequestMapping("/api/categories")
@RequiredArgsConstructor
public class CategoryController {

    private final CategoryService categoryService;

    /**
     * Retrieves a list of all vehicle categories.
     * This is a public endpoint typically used for populating UI dropdowns and filters.
     *
     * @return A list of CategoryResponse objects.
     */
    @GetMapping
    public ResponseEntity<List<CategoryResponse>> getAllCategories() {

        log.info("Fetching all vehicle categories");

        return ResponseEntity.ok(categoryService.getAllCategories());
    }

    /**
     * Creates a new vehicle category.
     * Restricted to users with the ADMIN authority.
     *
     * @param request The validated payload containing the new category's details.
     * @return The created CategoryResponse object.
     */
    @PostMapping
    @PreAuthorize("hasAuthority('ADMIN')")
    public ResponseEntity<CategoryResponse> createCategory(@Valid @RequestBody CategoryRequest request) {

        log.info("Admin request to create new category: {}", request.getName());

        return ResponseEntity.ok(categoryService.createCategory(request));
    }

    /**
     * Updates an existing vehicle category.
     * Restricted to users with the ADMIN authority.
     *
     * @param id      The unique identifier of the category to update.
     * @param request The validated payload containing the updated details.
     * @return The updated CategoryResponse object.
     */
    @PutMapping("/{id}")
    @PreAuthorize("hasAuthority('ADMIN')")
    public ResponseEntity<CategoryResponse> updateCategory(
            @PathVariable Long id,
            @Valid @RequestBody CategoryRequest request) {

        log.info("Admin request to update category ID: {} with new name: {}", id, request.getName());

        return ResponseEntity.ok(categoryService.updateCategory(id, request));
    }
}