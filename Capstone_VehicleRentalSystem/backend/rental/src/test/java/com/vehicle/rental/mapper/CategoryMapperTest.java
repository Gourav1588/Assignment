package com.vehicle.rental.mapper;

import com.vehicle.rental.dto.request.CategoryRequest;
import com.vehicle.rental.dto.response.CategoryResponse;
import com.vehicle.rental.entity.VehicleCategory;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Unit tests for the CategoryMapper.
 */
class CategoryMapperTest {

    private CategoryMapper categoryMapper;

    @BeforeEach
    void setUp() {
        categoryMapper = new CategoryMapper();
    }

    /**
     * Tests mapping from a request DTO to an entity.
     * Verifies that whitespace is properly trimmed from the category name.
     */
    @Test
    void shouldMapRequestToEntityAndTrimWhitespace() {
        // Given
        CategoryRequest request = new CategoryRequest();
        request.setName("  Luxury SUVs  "); // Notice the extra spaces
        request.setDescription("High-end sports utility vehicles");

        // When
        VehicleCategory entity = categoryMapper.toEntity(request);

        // Then
        assertNotNull(entity);
        assertEquals("Luxury SUVs", entity.getName(), "Whitespace should be trimmed from the name");
        assertEquals("High-end sports utility vehicles", entity.getDescription());
    }

    /**
     * Tests mapping from the database entity back to the response DTO.
     */
    @Test
    void shouldMapEntityToResponse() {
        // Given
        VehicleCategory category = new VehicleCategory();
        category.setId(10L);
        category.setName("Hatchback");
        category.setDescription("Compact city cars");

        // When
        CategoryResponse response = categoryMapper.toResponse(category);

        // Then
        assertNotNull(response);
        assertEquals(10L, response.getId());
        assertEquals("Hatchback", response.getName());
        assertEquals("Compact city cars", response.getDescription());
    }
}