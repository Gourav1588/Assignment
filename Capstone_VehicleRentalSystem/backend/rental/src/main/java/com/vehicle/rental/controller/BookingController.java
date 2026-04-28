package com.vehicle.rental.controller;

import com.vehicle.rental.dto.request.BookingRequest;
import com.vehicle.rental.dto.response.ApiResponse;
import com.vehicle.rental.dto.response.BookingResponse;
import com.vehicle.rental.entity.Booking.BookingStatus;
import com.vehicle.rental.security.CustomUserDetails;
import com.vehicle.rental.service.BookingService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

@Slf4j
@RestController
@RequestMapping("/api/bookings")
@CrossOrigin(origins = "*")
@RequiredArgsConstructor
public class BookingController {

    // Service layer to handle business logic
    private final BookingService bookingService;

    // Create a new booking (User)
    // Retrieves logged-in user from security context
    // Returns booking in PENDING state for confirmation
    @PostMapping
    public ResponseEntity<BookingResponse> createBooking(
            @AuthenticationPrincipal CustomUserDetails userDetails,
            @Valid @RequestBody BookingRequest request) {

        // Extract user ID from authenticated user
        Long userId = userDetails.getUser().getId();

        // Delegate booking creation to service layer
        return ResponseEntity.ok(
                bookingService.createBooking(userId, request));
    }

    // Confirm a booking (User)
    // Changes status from PENDING → ACTIVE
    @PutMapping("/{id}/confirm")
    public ResponseEntity<BookingResponse> confirmBooking(
            @PathVariable Long id,
            @AuthenticationPrincipal CustomUserDetails userDetails) {

        Long userId = userDetails.getUser().getId();

        return ResponseEntity.ok(
                bookingService.confirmBooking(id, userId));
    }

    // Cancel a booking (User)
    // Changes status to CANCELLED if allowed
    @PutMapping("/{id}/cancel")
    public ResponseEntity<BookingResponse> cancelBooking(
            @PathVariable Long id,
            @AuthenticationPrincipal CustomUserDetails userDetails) {

        Long userId = userDetails.getUser().getId();

        return ResponseEntity.ok(
                bookingService.cancelBooking(id, userId));
    }

    // Fetch bookings of the logged-in user
    // Supports pagination for efficient data retrieval
    @GetMapping("/my")
    public ResponseEntity<Page<BookingResponse>> myBookings(
            @AuthenticationPrincipal CustomUserDetails userDetails,
            @RequestParam(defaultValue = "0")  int page,
            @RequestParam(defaultValue = "10") int size) {

        Long userId = userDetails.getUser().getId();

        return ResponseEntity.ok(
                bookingService.getUserBookings(userId, page, size));
    }

    // Fetch all bookings (Admin only)
    // Restricted using role-based authorization
    @GetMapping
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<Page<BookingResponse>> getAllBookings(
            @RequestParam(defaultValue = "0")  int page,
            @RequestParam(defaultValue = "10") int size) {

        return ResponseEntity.ok(
                bookingService.getAllBookings(page, size));
    }




}