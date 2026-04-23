package com.vehicle.rental.service;

import com.vehicle.rental.dto.request.LoginRequest;
import com.vehicle.rental.dto.request.RegisterRequest;
import com.vehicle.rental.entity.User;
import com.vehicle.rental.exception.BadRequestException;
import com.vehicle.rental.repository.UserRepository;
import com.vehicle.rental.security.JwtService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Slf4j
@Service
@RequiredArgsConstructor
public class AuthService {

    // Handles DB operations for User
    private final UserRepository userRepository;

    // Used to hash and verify passwords
    private final PasswordEncoder passwordEncoder;

    // Used to generate JWT tokens
    private final JwtService jwtService;

    // Register new user
    @Transactional
    public String register(RegisterRequest request) {

        log.debug("Register attempt for: {}", request.getEmail());

        // Check if email already exists
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new BadRequestException("Email already registered");
        }

        // Create new user entity
        User user = new User();
        user.setName(request.getName().trim()); // remove extra spaces
        user.setEmail(request.getEmail().trim().toLowerCase()); // normalize email
        user.setPassword(passwordEncoder.encode(request.getPassword())); // hash password
        user.setRole(User.Role.USER); // default role

        // Save user in database
        userRepository.save(user);

        log.debug("User registered successfully: {}", request.getEmail());

        // Generate JWT token and return it
        return jwtService.generateToken(user);
    }

    // Login existing user
    public String login(LoginRequest request) {

        log.debug("Login attempt for: {}", request.getEmail());

        // Fetch user by email
        // Same error message used for security (avoid revealing which part is wrong)
        User user = userRepository
                .findByEmail(request.getEmail().trim().toLowerCase())
                .orElseThrow(() -> new BadRequestException(
                        "Invalid email or password"
                ));

        // Check password
        if (!passwordEncoder.matches(
                request.getPassword(), user.getPassword())) {

            throw new BadRequestException(" password");
        }

        log.debug("Login successful for: {}", request.getEmail());

        // Generate JWT token and return it
        return jwtService.generateToken(user);
    }
}