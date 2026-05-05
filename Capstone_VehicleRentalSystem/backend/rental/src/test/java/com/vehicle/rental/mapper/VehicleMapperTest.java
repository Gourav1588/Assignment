package com.vehicle.rental.mapper;

import com.vehicle.rental.dto.request.VehicleRequest;
import com.vehicle.rental.dto.response.VehicleResponse;
import com.vehicle.rental.entity.Vehicle;
import com.vehicle.rental.entity.VehicleCategory;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Unit tests for the VehicleMapper.
 * Validates data transformations including string standardization and safe nested extractions.
 */
class VehicleMapperTest {

    private VehicleMapper vehicleMapper;

    @BeforeEach
    void setUp() {
        vehicleMapper = new VehicleMapper();
    }

    /**
     * Tests the mapping of user input (Request) to the Vehicle entity.
     * Crucially checks if the registration number is capitalized and trimmed.
     */
    @Test
    void shouldMapRequestToEntityWithFormatting() {
        // Given
        VehicleRequest request = new VehicleRequest();
        request.setRegistrationNumber(" ka-01-ab-1234 "); // Lowercase with spaces
        request.setName(" Honda Civic ");
        request.setType(Vehicle.VehicleType.CAR);
        request.setPricePerDay(1500.0);
        request.setDescription("A reliable sedan");

        // When
        Vehicle entity = vehicleMapper.toEntity(request);

        // Then
        assertNotNull(entity);
        assertEquals("KA-01-AB-1234", entity.getRegistrationNumber(), "Registration number should be uppercase and trimmed");
        assertEquals("Honda Civic", entity.getName(), "Name should be trimmed");
        assertEquals(Vehicle.VehicleType.CAR, entity.getType());
        assertEquals(1500.0, entity.getPricePerDay());
        assertTrue(entity.isActive(), "New vehicles should be set to active by default");
    }

    /**
     * Tests mapping to a response when a category is attached.
     */
    @Test
    void shouldMapEntityToResponseWithCategory() {
        // Given
        VehicleCategory category = new VehicleCategory();
        category.setName("Sedan");

        Vehicle vehicle = new Vehicle();
        vehicle.setId(5L);
        vehicle.setRegistrationNumber("DL-8C-9999");
        vehicle.setName("Hyundai Verna");
        vehicle.setType(Vehicle.VehicleType.CAR);
        vehicle.setPricePerDay(2000.0);
        vehicle.setDescription("Premium interior");
        vehicle.setActive(true);
        vehicle.setCategory(category); // Attaching the category

        // When
        VehicleResponse response = vehicleMapper.toResponse(vehicle);

        // Then
        assertNotNull(response);
        assertEquals(5L, response.getId());
        assertEquals("DL-8C-9999", response.getRegistrationNumber());
        assertEquals("Sedan", response.getCategoryName(), "Category name should be safely extracted");
    }

    /**
     * Tests that the mapper doesn't throw a NullPointerException if a vehicle has no category.
     */
    @Test
    void shouldMapEntityToResponseWithoutCategory() {
        // Given
        Vehicle vehicle = new Vehicle();
        vehicle.setName("Yamaha R15");
        vehicle.setCategory(null); // Explicitly null

        // When
        VehicleResponse response = vehicleMapper.toResponse(vehicle);

        // Then
        assertNotNull(response);
        assertNull(response.getCategoryName(), "Category name should be null without throwing exceptions");
    }
}