package com.vehicle.rental.controller;

import com.vehicle.rental.dto.request.CategoryRequest;
import com.vehicle.rental.dto.response.ApiResponse;
import com.vehicle.rental.dto.response.CategoryResponse;
import com.vehicle.rental.service.CategoryService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/categories")
@CrossOrigin(origins = "*")
@RequiredArgsConstructor
public class CategoryController {

    // Service layer to handle business logic
    private final CategoryService categoryService;

    // Fetch all categories
    // Public endpoint used for listing or dropdowns
    @GetMapping
    public ResponseEntity<List<CategoryResponse>> getAllCategories() {

        // Service already returns DTO list, no mapping required here
        return ResponseEntity.ok(
                categoryService.getAllCategories()
        );
    }

    // Create a new category (Admin only)
    // Accepts validated request DTO and returns response DTO
    @PostMapping
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<CategoryResponse> createCategory(
            @Valid @RequestBody CategoryRequest request) {

        // Delegate creation to service layer
        return ResponseEntity.ok(
                categoryService.createCategory(request)
        );
    }

    // Update an existing category (Admin only)
    // Uses DTO for safe and controlled updates
    @PutMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<CategoryResponse> updateCategory(
            @PathVariable Long id,
            @Valid @RequestBody CategoryRequest request) {

        return ResponseEntity.ok(
                categoryService.updateCategory(id, request)
        );
    }

    // Delete a category (Admin only)
    // Performs validation before deletion (handled in service)
    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<ApiResponse> deleteCategory(
            @PathVariable Long id) {

        categoryService.deleteCategory(id);

        // Return standardized success response
        return ResponseEntity.ok(
                new ApiResponse(
                        "Category deleted successfully",
                        true
                )
        );
    }
}