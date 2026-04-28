package com.vehicle.rental.mapper;

import com.vehicle.rental.dto.response.UserResponse;
import com.vehicle.rental.entity.User;
import org.springframework.stereotype.Component;

/**
 * Utility component for mapping User entities to Data Transfer Objects.
 */
@Component
public class UserMapper {

    /**
     * Converts a database User entity into a safe UserResponse DTO.
     *
     * @param user The database entity.
     * @return The formatted response object (excludes sensitive data like passwords).
     */
    public UserResponse toResponse(User user) {
        if (user == null) {
            return null;
        }

        return new UserResponse(
                user.getId(),
                user.getName(),
                user.getEmail(),
                user.getRole().name()
        );
    }
}