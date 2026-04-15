package com.nucleusteq.session3.controller;

import com.nucleusteq.session3.model.User;
import com.nucleusteq.session3.service.UserService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.http.HttpStatus;

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


    @PostMapping("/submit")
    public ResponseEntity<String> submitUser(@RequestBody User user) {

        // Let the service handle validation and business logic
        String result = userService.validateAndSubmit(user);

        // If validation fails, return a 400 Bad Request
        if ("invalid".equalsIgnoreCase(result)) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                    .body("Invalid input. Please provide a valid id , name, age, and role.");
        }

        // If everything is fine, return 201 Created
        return ResponseEntity.status(HttpStatus.CREATED)
                .body("User submitted successfully.");
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<String> deleteUser(
            @PathVariable int id,
            @RequestParam(required = false) Boolean confirm) {

        String response = userService.deleteUser(id, confirm);
        return ResponseEntity.ok(response);
    }
}