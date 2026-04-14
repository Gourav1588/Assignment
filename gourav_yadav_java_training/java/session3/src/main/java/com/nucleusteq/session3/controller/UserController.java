package com.nucleusteq.session3.controller;

import com.nucleusteq.session3.model.User;
import com.nucleusteq.session3.service.UserService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * Handles user-related API requests.
 */
@RestController
@RequestMapping("/users")
public class UserController {

    // Business logic layer
    private final UserService userService;

    // Inject UserService
    public UserController(UserService userService) {
        this.userService = userService;
    }

    /**
     * GET /users/search
     * Returns users filtered by optional params (AND condition).
     */
    @GetMapping("/search")
    public ResponseEntity<List<User>> searchUsers(
            @RequestParam(required = false) String name,
            @RequestParam(required = false) Integer age,
            @RequestParam(required = false) String role) {

        // Delegate filtering to service
        List<User> result = userService.searchUsers(name, age, role);

        // Return response
        return ResponseEntity.ok(result);
    }
}