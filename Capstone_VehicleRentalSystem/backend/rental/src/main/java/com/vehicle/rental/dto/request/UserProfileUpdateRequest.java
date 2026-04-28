package com.vehicle.rental.dto.request;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Data Transfer Object for handling user profile update requests.
 * All fields are optional to support partial updates.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class UserProfileUpdateRequest {

    /**
     * The updated name of the user. Can be null if no change is requested.
     */
    private String name;

    /**
     * The new raw password. Can be null or empty if the user is not changing their password.
     */
    private String password;
}