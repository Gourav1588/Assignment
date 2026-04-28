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

/**
 * REST Controller managing vehicle booking operations.
 * Handles creating, confirming, and canceling bookings, as well as retrieving user and system-wide booking history.
 */
@Slf4j
@RestController
@RequestMapping("/api/bookings")
@RequiredArgsConstructor
public class BookingController {

    private final BookingService bookingService;

    /**
     * Creates a new booking for the authenticated user.
     * The initial state of the booking will be set to PENDING pending confirmation.
     *
     * @param userDetails The security context containing the authenticated user's details.
     * @param request     The booking payload containing vehicle details and rental dates.
     * @return The created BookingResponse object.
     */
    @PostMapping
    public ResponseEntity<BookingResponse> createBooking(
            @AuthenticationPrincipal CustomUserDetails userDetails,
            @Valid @RequestBody BookingRequest request) {

        Long userId = userDetails.getUser().getId();
        log.info("Processing booking creation request for user ID: {}", userId);

        return ResponseEntity.ok(bookingService.createBooking(userId, request));
    }

    /**
     * Confirms a pending booking.
     * Transitions the booking status from PENDING to ACTIVE.
     *
     * @param id          The unique identifier of the booking to confirm.
     * @param userDetails The security context containing the authenticated user's details.
     * @return The updated BookingResponse object.
     */
    @PutMapping("/{id}/confirm")
    public ResponseEntity<BookingResponse> confirmBooking(
            @PathVariable Long id,
            @AuthenticationPrincipal CustomUserDetails userDetails) {

        Long userId = userDetails.getUser().getId();
        log.info("Confirming booking ID: {} for user ID: {}", id, userId);

        return ResponseEntity.ok(bookingService.confirmBooking(id, userId));
    }

    /**
     * Cancels an existing booking.
     * Transitions the booking status to CANCELLED if business rules allow it.
     *
     * @param id          The unique identifier of the booking to cancel.
     * @param userDetails The security context containing the authenticated user's details.
     * @return The updated BookingResponse object.
     */
    @PutMapping("/{id}/cancel")
    public ResponseEntity<BookingResponse> cancelBooking(
            @PathVariable Long id,
            @AuthenticationPrincipal CustomUserDetails userDetails) {

        Long userId = userDetails.getUser().getId();
        log.info("Cancelling booking ID: {} for user ID: {}", id, userId);

        return ResponseEntity.ok(bookingService.cancelBooking(id, userId));
    }

    /**
     * Retrieves a paginated list of bookings belonging to the authenticated user.
     *
     * @param userDetails The security context containing the authenticated user's details.
     * @param page        The page number to retrieve (0-based indexing).
     * @param size        The number of records per page.
     * @return A paginated list of the user's BookingResponse objects.
     */
    @GetMapping("/my")
    public ResponseEntity<Page<BookingResponse>> myBookings(
            @AuthenticationPrincipal CustomUserDetails userDetails,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size) {

        Long userId = userDetails.getUser().getId();
        return ResponseEntity.ok(bookingService.getUserBookings(userId, page, size));
    }

    /**
     * Retrieves a paginated list of all bookings in the system.
     * Restricted to users with the ADMIN authority.
     *
     * @param page The page number to retrieve (0-based indexing).
     * @param size The number of records per page.
     * @return A paginated list of all BookingResponse objects.
     */
    @GetMapping
    @PreAuthorize("hasAuthority('ADMIN')")
    public ResponseEntity<Page<BookingResponse>> getAllBookings(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size) {

        return ResponseEntity.ok(bookingService.getAllBookings(page, size));
    }
}