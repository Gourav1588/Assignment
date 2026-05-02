package com.vehicle.rental.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.vehicle.rental.dto.request.UserProfileUpdateRequest;
import com.vehicle.rental.dto.response.UserResponse;
import com.vehicle.rental.entity.User;
import com.vehicle.rental.repository.UserRepository;
import com.vehicle.rental.security.CustomUserDetails;
import com.vehicle.rental.security.JwtService;
import com.vehicle.rental.service.UserService;
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
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

/**
 * Web Layer tests for the {@link UserController}.
 * Validates admin retrieval and secure user profile updates.
 */
@WebMvcTest(UserController.class)
class UserControllerTest {

    /**
     * TEST SECURITY CONFIGURATION
     * Bypasses strict Web Security filters (like CSRF) to allow MockMvc to reach
     * the controller, while keeping the Security Context active so that the
     * Principal object is correctly injected into the controller methods.
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
    private UserService userService;

    // Required to satisfy the global security context auto-configuration
    @MockBean private JwtService jwtService;
    @MockBean private UserRepository userRepository;

    private UserResponse testResponse;
    private UserProfileUpdateRequest testRequest;
    private CustomUserDetails mockUserDetails;
    private CustomUserDetails adminUserDetails;

    @BeforeEach
    void setUp() {
        // 1. Build a regular User Principal
        User regularUser = new User();
        regularUser.setId(1L);
        regularUser.setEmail("test@driveeasy.com");
        regularUser.setRole(User.Role.USER);
        mockUserDetails = new CustomUserDetails(regularUser);

        // 2. Build an Admin User Principal
        User adminUser = new User();
        adminUser.setId(2L);
        adminUser.setEmail("admin@driveeasy.com");
        adminUser.setRole(User.Role.ADMIN);
        adminUserDetails = new CustomUserDetails(adminUser);

        // 3. Build test DTOs
        testResponse = new UserResponse();
        testResponse.setId(1L);
        testResponse.setEmail("test@driveeasy.com");
        testResponse.setName("Gourav Yadav");

        testRequest = new UserProfileUpdateRequest();
        testRequest.setName("Gourav Updated");
        testRequest.setPassword("newSecurePassword123");
    }

    @Test
    void getAllUsers_Admin_Returns200() throws Exception {
        // Arrange
        when(userService.getAllUsersForAdmin()).thenReturn(List.of(testResponse));

        // Act & Assert
        mockMvc.perform(get("/api/users")
                        .with(user(adminUserDetails))) // Authenticate as Admin
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].email").value("test@driveeasy.com"));
    }

    @Test
    void updateProfile_Returns200AndSuccessMessage() throws Exception {
        // Arrange
        when(userService.updateProfile(eq("test@driveeasy.com"), any(UserProfileUpdateRequest.class)))
                .thenReturn(testResponse);

        // Act & Assert
        // The .with(user()) automatically translates into the "Principal" argument in your controller!
        mockMvc.perform(put("/api/users/profile")
                        .with(user(mockUserDetails))
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(testRequest)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.message").value("Profile updated successfully"));
    }
}