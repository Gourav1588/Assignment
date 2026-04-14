package com.nucleusteq.session3.service;

import com.nucleusteq.session3.model.User;
import com.nucleusteq.session3.repository.UserRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

/**
 * Service layer to handle business logic for user-related operations.
 */
@Service
public class UserService {

    private final UserRepository userRepository;

    /**
     * This ensures that Spring manages the UserRepository lifecycle.
     */
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    /**
     * Main filtering logic for the user search API.
     * It handles multiple parameters and applies logic like case-insensitivity.
     */
    public List<User> searchUsers(String name, Integer age, String role) {
        // Fetch the initial set of 5-7 dummy users from the repository
        List<User> result = userRepository.findAll();

        // If 'name' is provided, filter the list ignoring case.
        if (name != null) {
            result = result.stream()
                    .filter(u -> u.getName().equalsIgnoreCase(name))
                    .collect(Collectors.toList());
        }

        // Apply an exact match filter for age if the parameter is present.
        if (age != null) {
            result = result.stream()
                    .filter(u -> u.getAge()==(age))
                    .collect(Collectors.toList());
        }

        // Filter by role ignoring case to ensure flexibility (e.g., "USER" vs "user").
        if (role != null) {
            result = result.stream()
                    .filter(u -> u.getRole().equalsIgnoreCase(role))
                    .collect(Collectors.toList());
        }

        // Returns all users if no parameters were passed, or the filtered list otherwise.
        return result;
    }
}