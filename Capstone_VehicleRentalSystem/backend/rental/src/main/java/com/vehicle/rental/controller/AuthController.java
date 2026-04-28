package com.vehicle.rental.controller;

import com.vehicle.rental.dto.request.LoginRequest;
import com.vehicle.rental.dto.request.RegisterRequest;
import com.vehicle.rental.dto.response.ApiResponse;
import com.vehicle.rental.service.AuthService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * REST Controller managing authentication operations.
 * Handles user registration and login, issuing JWT tokens upon success.
 */
@Slf4j
@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
public class AuthController {

    private final AuthService authService;

    /**
     * Registers a new user account and generates an initial JWT token.
     *
     * @param request The registration payload containing user details (name, email, password).
     * @return An API response containing the success message and JWT token.
     */
    @PostMapping("/register")
    public ResponseEntity<ApiResponse> register(@Valid @RequestBody RegisterRequest request) {

        log.info("Processing registration request for email: {}", request.getEmail());
        String token = authService.register(request);

        return ResponseEntity.ok(new ApiResponse("Registration successful", token));
    }

    /**
     * Authenticates an existing user and generates a new session JWT token.
     *
     * @param request The login payload containing user credentials.
     * @return An API response containing the success message and JWT token.
     */
    @PostMapping("/login")
    public ResponseEntity<ApiResponse> login(@Valid @RequestBody LoginRequest request) {

        log.info("Processing login request for email: {}", request.getEmail());
        String token = authService.login(request);

        return ResponseEntity.ok(new ApiResponse("Login successful", token));
    }
}