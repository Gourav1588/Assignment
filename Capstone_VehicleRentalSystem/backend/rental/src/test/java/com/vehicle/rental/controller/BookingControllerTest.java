package com.vehicle.rental.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.vehicle.rental.dto.request.BookingRequest;
import com.vehicle.rental.dto.response.BookingResponse;
import com.vehicle.rental.entity.Booking.BookingStatus;
import com.vehicle.rental.entity.User;
import com.vehicle.rental.repository.UserRepository;
import com.vehicle.rental.security.CustomUserDetails;
import com.vehicle.rental.security.JwtService;
import com.vehicle.rental.service.BookingService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Bean;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.PageRequest;
import org.springframework.http.MediaType;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.test.web.servlet.MockMvc;

import java.time.LocalDateTime;
import java.util.List;

import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.when;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.user;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(BookingController.class)
class BookingControllerTest {

    /**
     * TEST SECURITY CONFIGURATION
     * This safely overrides your real SecurityConfig just for this test.
     * It disables CSRF and permits all requests to prevent 403 Forbidden errors,
     * while keeping the SecurityContext alive so @AuthenticationPrincipal works.
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
    private BookingService bookingService;

    // Kept to prevent Spring context from crashing if auto-wiring attempts to find them
    @MockBean private JwtService jwtService;
    @MockBean private UserRepository userRepository;

    private BookingResponse testResponse;
    private BookingRequest testRequest;
    private CustomUserDetails mockUserDetails;

    @BeforeEach
    void setUp() {
        // Build the mock user that will be injected into @AuthenticationPrincipal
        User user = new User();
        user.setId(1L);
        user.setEmail("test@driveeasy.com");
        user.setRole(User.Role.USER);
        mockUserDetails = new CustomUserDetails(user);

        // Build a reusable booking response
        testResponse = new BookingResponse();
        testResponse.setId(500L);
        testResponse.setVehicleName("Toyota Fortuner");
        testResponse.setTotalCost(12000.0);
        testResponse.setStatus(BookingStatus.PENDING);

        // Build a valid booking request
        testRequest = new BookingRequest();
        testRequest.setVehicleId(100L);
        testRequest.setStartTime(LocalDateTime.now().plusDays(1));
        testRequest.setEndTime(LocalDateTime.now().plusDays(3));
    }

    @Test
    void createBooking_Returns200() throws Exception {
        when(bookingService.createBooking(eq(1L), any(BookingRequest.class))).thenReturn(testResponse);

        mockMvc.perform(post("/api/bookings")
                        .with(user(mockUserDetails)) // Injects user directly into the controller
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(testRequest)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.vehicleName").value("Toyota Fortuner"));
    }

    @Test
    void confirmBooking_Returns200() throws Exception {
        when(bookingService.confirmBooking(eq(500L), eq(1L))).thenReturn(testResponse);

        mockMvc.perform(put("/api/bookings/500/confirm")
                        .with(user(mockUserDetails)))
                .andExpect(status().isOk());
    }

    @Test
    void cancelBooking_Returns200() throws Exception {
        when(bookingService.cancelBooking(eq(500L), eq(1L))).thenReturn(testResponse);

        mockMvc.perform(put("/api/bookings/500/cancel")
                        .with(user(mockUserDetails)))
                .andExpect(status().isOk());
    }

    @Test
    void myBookings_Returns200() throws Exception {
        Page<BookingResponse> page = new PageImpl<>(List.of(testResponse), PageRequest.of(0, 10), 1);
        when(bookingService.getUserBookings(eq(1L), anyInt(), anyInt())).thenReturn(page);

        mockMvc.perform(get("/api/bookings/my")
                        .with(user(mockUserDetails))
                        .param("page", "0")
                        .param("size", "10"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.content[0].vehicleName").value("Toyota Fortuner"));
    }

    @Test
    void getAllBookings_Admin_Returns200() throws Exception {
        // Create an Admin user for this specific test
        User admin = new User();
        admin.setId(2L);
        admin.setEmail("admin@driveeasy.com");
        admin.setRole(User.Role.ADMIN);
        CustomUserDetails adminDetails = new CustomUserDetails(admin);

        Page<BookingResponse> page = new PageImpl<>(List.of(testResponse), PageRequest.of(0, 10), 1);
        when(bookingService.getAllBookings(anyInt(), anyInt())).thenReturn(page);

        mockMvc.perform(get("/api/bookings")
                        .with(user(adminDetails))
                        .param("page", "0")
                        .param("size", "10"))
                .andExpect(status().isOk());
    }
}