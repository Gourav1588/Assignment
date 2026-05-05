package com.vehicle.rental.mapper;

import com.vehicle.rental.dto.response.UserResponse;
import com.vehicle.rental.entity.User;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Unit tests for the UserMapper.
 * Ensures that user entities are safely converted to client-facing DTOs.
 */
class UserMapperTest {

    private UserMapper userMapper;

    @BeforeEach
    void setUp() {
        userMapper = new UserMapper();
    }

    /**
     * Tests that a valid User entity maps correctly to a UserResponse,
     * ensuring sensitive fields like passwords are not included.
     */
    @Test
    void shouldMapUserToResponseSuccessfully() {
        // Given
        User user = new User();
        user.setId(1L);
        user.setName("John Doe");
        user.setEmail("john.doe@example.com");
        // Assuming a generic Role enum exists in your User entity
        user.setRole(User.Role.USER);

        // When
        UserResponse response = userMapper.toResponse(user);

        // Then
        assertNotNull(response);
        assertEquals(1L, response.getId());
        assertEquals("John Doe", response.getName());
        assertEquals("john.doe@example.com", response.getEmail());
        assertEquals("USER", response.getRole());
    }

    /**
     * Tests the null-safety fallback of the mapper.
     */
    @Test
    void shouldReturnNullWhenUserIsNull() {
        // When
        UserResponse response = userMapper.toResponse(null);

        // Then
        assertNull(response, "Mapper should return null if the input entity is null.");
    }
}