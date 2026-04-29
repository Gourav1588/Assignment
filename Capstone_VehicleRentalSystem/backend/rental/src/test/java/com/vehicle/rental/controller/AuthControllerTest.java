package com.vehicle.rental.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.vehicle.rental.dto.request.LoginRequest;
import com.vehicle.rental.dto.request.RegisterRequest;
import com.vehicle.rental.service.AuthService;
import com.vehicle.rental.security.JwtService;
import com.vehicle.rental.repository.UserRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

/**
 * Web Layer tests for the {@link AuthController}.
 * Uses MockMvc to simulate HTTP requests without starting a full server.
 */
@WebMvcTest(AuthController.class)
@AutoConfigureMockMvc(addFilters = false) // Bypasses Spring Security filters for this isolated test
class AuthControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper; // Used to convert our Java objects into JSON strings

    @MockBean // Note: In WebMvc tests, we use @MockBean instead of @Mock
    private AuthService authService;

    @MockBean
    private JwtService jwtService;

    @MockBean
    private UserRepository userRepository;

    private RegisterRequest registerRequest;
    private LoginRequest loginRequest;
    private final String MOCK_TOKEN = "mock.jwt.token.12345";

    @BeforeEach
    void setUp() {
        registerRequest = new RegisterRequest();
        registerRequest.setName("Test User");
        registerRequest.setEmail("test@driveeasy.com");
        registerRequest.setPassword("securePass123");

        loginRequest = new LoginRequest();
        loginRequest.setEmail("test@driveeasy.com");
        loginRequest.setPassword("securePass123");
    }

    @Test
    void register_Returns200AndToken() throws Exception {
        // Arrange: Tell our mocked service what to return
        when(authService.register(any(RegisterRequest.class))).thenReturn(MOCK_TOKEN);

        // Act & Assert: Simulate a web browser sending a POST request
        mockMvc.perform(post("/api/auth/register")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(registerRequest))) // Convert Java to JSON
                .andExpect(status().isOk()) // Expect HTTP 200
                .andExpect(jsonPath("$.message").value("Registration successful")); // Verify JSON response
    }

    @Test
    void login_Returns200AndToken() throws Exception {
        // Arrange
        when(authService.login(any(LoginRequest.class))).thenReturn(MOCK_TOKEN);

        // Act & Assert
        mockMvc.perform(post("/api/auth/login")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(loginRequest)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.message").value("Login successful"));
    }
}