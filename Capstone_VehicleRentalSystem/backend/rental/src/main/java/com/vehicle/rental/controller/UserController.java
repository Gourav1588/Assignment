package com.vehicle.rental.controller;

import com.vehicle.rental.dto.request.UserProfileUpdateRequest;
import com.vehicle.rental.dto.response.UserResponse;
import com.vehicle.rental.service.UserService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.security.Principal;
import java.util.List;
import java.util.Map;

/**
 * REST Controller for managing user data and profile operations.
 */
@Slf4j
@RestController
@RequestMapping("/api/users")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    /**
     * Retrieves a list of all registered users.
     * Restricted to users with the ADMIN authority.
     *
     * @return A list of user responses.
     */
    @GetMapping
    @PreAuthorize("hasAuthority('ADMIN')")
    public ResponseEntity<List<UserResponse>> getAllUsers() {

        log.info("Admin request to fetch all registered users");

        List<UserResponse> safeUsers = userService.getAllUsersForAdmin();
        return ResponseEntity.ok(safeUsers);
    }

    /**
     * Updates the authenticated user's profile settings.
     * Extracts the user's identity securely from the Principal object.
     *
     * @param request   The update payload.
     * @param principal The security principal representing the authenticated user.
     * @return A success message mapping.
     */
    @PutMapping("/profile")
    public ResponseEntity<?> updateProfile(@RequestBody UserProfileUpdateRequest request, Principal principal) {

        // Extract the authenticated user's email directly from the security context
        String loggedInEmail = principal.getName();

        log.info("Processing profile update request for user: {}", loggedInEmail);

        // Execute business logic
        userService.updateProfile(loggedInEmail, request);

        // Return structured JSON response confirming the update
        return ResponseEntity.ok(Map.of("message", "Profile updated successfully"));
    }
}