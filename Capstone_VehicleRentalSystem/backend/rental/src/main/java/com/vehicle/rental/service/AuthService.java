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

/**
 * Service layer orchestrating user authentication and registration logic.
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class AuthService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtService jwtService;

    /**
     * Processes new user registrations.
     * Enforces email uniqueness, normalizes input, safely hashes the password using BCrypt,
     * and automatically issues an initial login token.
     */
    @Transactional
    public String register(RegisterRequest request) {
        log.debug("Initiating registration for email: {}", request.getEmail());

        if (userRepository.existsByEmail(request.getEmail())) {
            throw new BadRequestException("Email already registered");
        }

        User user = new User();
        user.setName(request.getName().trim());
        user.setEmail(request.getEmail().trim().toLowerCase());
        user.setPassword(passwordEncoder.encode(request.getPassword()));
        user.setRole(User.Role.USER);

        userRepository.save(user);
        log.info("New user account created successfully: {}", user.getEmail());

        return jwtService.generateToken(user);
    }

    /**
     * Processes user login attempts.
     * Utilizes a generic error message for both unrecognized emails and invalid passwords
     * to prevent account enumeration attacks.
     */
    public String login(LoginRequest request) {
        log.debug("Authenticating login request for: {}", request.getEmail());

        User user = userRepository
                .findByEmail(request.getEmail().trim().toLowerCase())
                .orElseThrow(() -> new BadRequestException("Invalid email or password"));

        if (!passwordEncoder.matches(request.getPassword(), user.getPassword())) {
            log.warn("Failed login attempt for email: {}", request.getEmail());
            throw new BadRequestException("Invalid email or password");
        }

        return jwtService.generateToken(user);
    }
}