package com.vehicle.rental.dto.request;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.Data;

/**
 * Data Transfer Object for new user registration.
 * Captures and validates the required personal details when a user creates a new account.
 */
@Data
public class RegisterRequest {

    /**
     * The full name of the user.
     * This field is mandatory and cannot be blank.
     */
    @NotBlank(message = "Name is required")
    private String name;

    /**
     * The email address of the user, which will serve as their primary identifier for logging in.
     * Must be a well-formed email string and cannot be blank.
     */
    @NotBlank(message = "Email is required")
    @Email(message = "Invalid email format")
    private String email;

    /**
     * The raw password chosen by the user.
     * Must not be blank and enforces a minimum length to meet basic security standards.
     */
    @NotBlank(message = "Password is required")
    @Size(min = 6, message = "Password must be at least 6 characters")
    private String password;
}