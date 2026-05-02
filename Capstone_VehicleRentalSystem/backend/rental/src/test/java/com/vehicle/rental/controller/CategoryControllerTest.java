package com.vehicle.rental.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.vehicle.rental.dto.request.CategoryRequest;
import com.vehicle.rental.dto.response.CategoryResponse;
import com.vehicle.rental.entity.User;
import com.vehicle.rental.repository.UserRepository;
import com.vehicle.rental.security.CustomUserDetails;
import com.vehicle.rental.security.JwtService;
import com.vehicle.rental.service.CategoryService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Bean;
import org.springframework.http.MediaType;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.test.web.servlet.MockMvc;

import java.util.List;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.when;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.user;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

/**
 * Web Layer tests for the {@link CategoryController}.
 * Validates public retrieval endpoints and secure administrative mutation endpoints.
 */
@WebMvcTest(CategoryController.class)
class CategoryControllerTest {

    /**
     * TEST SECURITY CONFIGURATION
     * Bypasses the strict JWT stateless configuration for testing purposes.
     * Disables CSRF and opens all routes so MockMvc can hit the controller methods
     * without throwing 401/403 errors.
     */
    @TestConfiguration
    static class TestSecurityConfig {
        @Bean
        public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
            http.csrf(csrf -> csrf.disable())
                    .authorizeHttpRequests(auth -> auth.anyRequest().permitAll());
            return http.build();
        }
    }

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockBean
    private CategoryService categoryService;

    // Required to prevent Spring Application Context from crashing
    @MockBean private JwtService jwtService;
    @MockBean private UserRepository userRepository;

    private CategoryResponse testResponse;
    private CategoryRequest testRequest;
    private CustomUserDetails adminUserDetails;

    @BeforeEach
    void setUp() {
        // Build an Admin User to pass the @PreAuthorize("hasAuthority('ADMIN')") checks
        User admin = new User();
        admin.setId(1L);
        admin.setEmail("admin@driveeasy.com");
        admin.setRole(User.Role.ADMIN);
        adminUserDetails = new CustomUserDetails(admin);

        testResponse = new CategoryResponse();
        testResponse.setId(10L);
        testResponse.setName("SUVs");
        testResponse.setDescription("Sport Utility Vehicles");

        testRequest = new CategoryRequest();
        testRequest.setName("SUVs");
        testRequest.setDescription("Sport Utility Vehicles");
    }

    @Test
    void getAllCategories_Returns200() throws Exception {
        // Arrange
        when(categoryService.getAllCategories()).thenReturn(List.of(testResponse));

        // Act & Assert
        mockMvc.perform(get("/api/categories"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].name").value("SUVs"));
    }

    @Test
    void createCategory_Returns200() throws Exception {
        // Arrange
        when(categoryService.createCategory(any(CategoryRequest.class))).thenReturn(testResponse);

        // Act & Assert
        mockMvc.perform(post("/api/categories")
                        .with(user(adminUserDetails)) // Pretend to be an admin
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(testRequest)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.name").value("SUVs"));
    }

    @Test
    void updateCategory_Returns200() throws Exception {
        // Arrange
        when(categoryService.updateCategory(eq(10L), any(CategoryRequest.class))).thenReturn(testResponse);

        // Act & Assert
        mockMvc.perform(put("/api/categories/10")
                        .with(user(adminUserDetails)) // Pretend to be an admin
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(testRequest)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.name").value("SUVs"));
    }
}