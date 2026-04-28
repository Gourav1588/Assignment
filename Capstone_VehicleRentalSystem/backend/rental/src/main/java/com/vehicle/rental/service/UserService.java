package com.vehicle.rental.service;

import com.vehicle.rental.dto.request.UserProfileUpdateRequest;
import com.vehicle.rental.dto.response.UserResponse;
import com.vehicle.rental.entity.User;
import com.vehicle.rental.mapper.UserMapper;
import com.vehicle.rental.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

/**
 * Service layer handling business logic for user management and profile operations.
 */
@Service
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final UserMapper userMapper;

    /**
     * Retrieves all users for administrative purposes.
     *
     * @return A list of safe UserResponse objects.
     */
    public List<UserResponse> getAllUsersForAdmin() {
        return userRepository.findAll()
                .stream()
                .map(userMapper::toResponse)
                .collect(Collectors.toList());
    }

    /**
     * Updates a user's profile information. Applies partial updates based on the provided request.
     *
     * @param email   The email of the authenticated user (extracted from JWT).
     * @param request The update payload containing new values.
     * @return The updated UserResponse.
     * @throws RuntimeException if the user is not found in the database.
     */
    @Transactional
    public UserResponse updateProfile(String email, UserProfileUpdateRequest request) {

        // 1. Validate entity existence
        User user = userRepository.findByEmail(email)
                .orElseThrow(() -> new RuntimeException("User not found"));

        // 2. Apply partial update: Name
        if (request.getName() != null && !request.getName().trim().isEmpty()) {
            user.setName(request.getName().trim());
        }

        // 3. Apply partial update: Password
        // Ensures the password is only updated if a valid, non-empty string is provided.
        if (request.getPassword() != null && !request.getPassword().trim().isEmpty()) {
            user.setPassword(passwordEncoder.encode(request.getPassword()));
        }

        // 4. Persist changes and map to response
        User updatedUser = userRepository.save(user);

        return userMapper.toResponse(updatedUser);
    }
}