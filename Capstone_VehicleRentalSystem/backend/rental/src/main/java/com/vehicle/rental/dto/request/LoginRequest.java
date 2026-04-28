package com.vehicle.rental.dto.request;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import lombok.Data;

/**
 * Data Transfer Object for user authentication.
 * Captures and validates the credentials provided by the user during the login process.
 */
@Data
public class LoginRequest {

    /**
     * The registered email address of the user.
     * Must be a well-formed email string and cannot be blank.
     */
    @NotBlank(message = "Email is required")
    @Email(message = "Invalid email format")
    private String email;

    /**
     * The raw password provided by the user for authentication.
     * Must not be blank.
     */
    @NotBlank(message = "Password is required")
    private String password;
}