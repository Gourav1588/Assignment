package com.vehicle.rental.service;

import com.vehicle.rental.dto.request.CategoryRequest;
import com.vehicle.rental.dto.response.CategoryResponse;
import com.vehicle.rental.entity.VehicleCategory;
import com.vehicle.rental.exception.BadRequestException;
import com.vehicle.rental.exception.ResourceNotFoundException;
import com.vehicle.rental.mapper.CategoryMapper;
import com.vehicle.rental.repository.CategoryRepository;
import com.vehicle.rental.repository.VehicleRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.*;

/**
 * Unit tests for the {@link CategoryService}.
 * Validates category creation, retrieval, and graceful handling of duplicates.
 */
@ExtendWith(MockitoExtension.class)
class CategoryServiceTest {

    @Mock
    private CategoryRepository categoryRepository;

    @Mock
    private VehicleRepository vehicleRepository; // Injected in service, so it must be mocked even if unused here

    @Mock
    private CategoryMapper categoryMapper;

    @InjectMocks
    private CategoryService categoryService;

    private VehicleCategory testCategory;
    private CategoryRequest testRequest;
    private CategoryResponse testResponse;

    @BeforeEach
    void setUp() {
        testCategory = new VehicleCategory();
        testCategory.setId(10L);
        testCategory.setName("SUVs");
        testCategory.setDescription("Sport Utility Vehicles");

        testRequest = new CategoryRequest();
        testRequest.setName(" SUVs "); // Added spaces to test the trim() logic
        testRequest.setDescription("Sport Utility Vehicles");

        testResponse = new CategoryResponse();
        testResponse.setId(10L);
        testResponse.setName("SUVs");
        testResponse.setDescription("Sport Utility Vehicles");
    }

    // =========================================================================
    // READ OPERATIONS
    // =========================================================================

    @Test
    void getAllCategories_Success() {
        when(categoryRepository.findAll()).thenReturn(List.of(testCategory));
        when(categoryMapper.toResponse(any(VehicleCategory.class))).thenReturn(testResponse);

        List<CategoryResponse> result = categoryService.getAllCategories();

        assertFalse(result.isEmpty());
        assertEquals(1, result.size());
        verify(categoryRepository, times(1)).findAll();
    }

    @Test
    void getCategoryById_Success() {
        // Note: This method returns the Entity directly, not the Response DTO
        when(categoryRepository.findById(10L)).thenReturn(Optional.of(testCategory));

        VehicleCategory result = categoryService.getCategoryById(10L);

        assertNotNull(result);
        assertEquals("SUVs", result.getName());
    }

    @Test
    void getCategoryById_NotFound_ThrowsException() {
        when(categoryRepository.findById(10L)).thenReturn(Optional.empty());

        assertThrows(ResourceNotFoundException.class, () -> categoryService.getCategoryById(10L));
    }

    // =========================================================================
    // CREATE OPERATIONS
    // =========================================================================

    @Test
    void createCategory_NewCategory_Success() {
        // Arrange: Category doesn't exist yet
        when(categoryRepository.findByNameIgnoreCase("SUVs")).thenReturn(Optional.empty());
        when(categoryMapper.toEntity(testRequest)).thenReturn(testCategory);
        when(categoryRepository.save(any(VehicleCategory.class))).thenReturn(testCategory);
        when(categoryMapper.toResponse(any(VehicleCategory.class))).thenReturn(testResponse);

        // Act
        CategoryResponse result = categoryService.createCategory(testRequest);

        // Assert
        assertNotNull(result);
        assertEquals("SUVs", result.getName());
        verify(categoryRepository, times(1)).save(any(VehicleCategory.class));
    }

    @Test
    void createCategory_ExistingCategory_ReturnsExisting() {
        // Arrange: Category already exists!
        when(categoryRepository.findByNameIgnoreCase("SUVs")).thenReturn(Optional.of(testCategory));
        when(categoryMapper.toResponse(any(VehicleCategory.class))).thenReturn(testResponse);

        // Act
        CategoryResponse result = categoryService.createCategory(testRequest);

        // Assert: We ensure the save() method was NEVER called to prevent duplicates
        assertNotNull(result);
        assertEquals("SUVs", result.getName());
        verify(categoryRepository, never()).save(any(VehicleCategory.class));
        verify(categoryMapper, never()).toEntity(any(CategoryRequest.class));
    }

    // =========================================================================
    // UPDATE OPERATIONS
    // =========================================================================

    @Test
    void updateCategory_Success_SameName() {
        // Arrange: Updating description, but keeping the name the same
        when(categoryRepository.findById(10L)).thenReturn(Optional.of(testCategory));
        when(categoryRepository.save(any(VehicleCategory.class))).thenReturn(testCategory);
        when(categoryMapper.toResponse(any(VehicleCategory.class))).thenReturn(testResponse);

        // Act
        CategoryResponse result = categoryService.updateCategory(10L, testRequest);

        // Assert
        assertNotNull(result);
        verify(categoryRepository, never()).existsByName(anyString()); // Shouldn't check DB if name didn't change
        verify(categoryRepository, times(1)).save(testCategory);
    }

    @Test
    void updateCategory_Success_NewName() {
        // Arrange: Changing the name to a brand new one
        testRequest.setName("Luxury Cars");
        when(categoryRepository.findById(10L)).thenReturn(Optional.of(testCategory));
        when(categoryRepository.existsByName("Luxury Cars")).thenReturn(false); // Name is free!
        when(categoryRepository.save(any(VehicleCategory.class))).thenReturn(testCategory);
        when(categoryMapper.toResponse(any(VehicleCategory.class))).thenReturn(testResponse);

        // Act
        CategoryResponse result = categoryService.updateCategory(10L, testRequest);

        // Assert
        assertNotNull(result);
        assertEquals("Luxury Cars", testCategory.getName()); // Proves the entity was updated before saving
        verify(categoryRepository, times(1)).existsByName("Luxury Cars");
        verify(categoryRepository, times(1)).save(testCategory);
    }

    @Test
    void updateCategory_DuplicateName_ThrowsException() {
        // Arrange: Changing the name, but the name is already taken!
        testRequest.setName("Sedans");
        when(categoryRepository.findById(10L)).thenReturn(Optional.of(testCategory));
        when(categoryRepository.existsByName("Sedans")).thenReturn(true); // Name is taken!

        // Act & Assert
        BadRequestException exception = assertThrows(BadRequestException.class, () -> {
            categoryService.updateCategory(10L, testRequest);
        });

        assertEquals("Category name already exists: Sedans", exception.getMessage());
        verify(categoryRepository, never()).save(any(VehicleCategory.class));
    }
}