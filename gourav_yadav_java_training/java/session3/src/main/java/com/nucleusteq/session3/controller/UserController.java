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

        boolean isValid = userService.validateAndSave(user);

        if (!isValid) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                    .body("Invalid input. Please provide valid id, name, age, and role.");
        }

        return ResponseEntity.status(HttpStatus.CREATED)
                .body("User submitted successfully.");
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<String> deleteUser(
            @PathVariable int id,
            @RequestParam(required = false) Boolean confirm) {

        String response = userService.deleteUser(id, confirm);
        if (response.equals("Confirmation required")) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(response);
        }
        return ResponseEntity.ok(response);
    }
}