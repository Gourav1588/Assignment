package com.vehicle.rental.mapper;

import com.vehicle.rental.dto.response.BookingResponse;
import com.vehicle.rental.entity.Booking;
import org.springframework.stereotype.Component;

import java.time.temporal.ChronoUnit;

@Component
public class BookingMapper {

    // Convert Booking entity to BookingResponse DTO
    // Transforms complex entity data into a flat, client-friendly format
    public BookingResponse toResponse(Booking booking) {

        // Create response object
        BookingResponse response = new BookingResponse();

        // Map basic booking identifier
        response.setId(booking.getId());

        // Map vehicle-related details
        // Extracts required fields from nested vehicle object
        response.setVehicleId(booking.getVehicle().getId());
        response.setVehicleName(booking.getVehicle().getName());
        response.setVehicleType(booking.getVehicle().getType().name());
        response.setPricePerDay(booking.getVehicle().getPricePerDay());

        // Map booking date details
        response.setStartDate(booking.getStartDate());
        response.setEndDate(booking.getEndDate());

        // Calculate total number of booking days (inclusive)
        // Adds +1 to include both start and end dates
        long days = ChronoUnit.DAYS.between(
                booking.getStartDate(),
                booking.getEndDate()
        ) + 1;
        response.setTotalDays(days);

        // Map total cost (already calculated and stored in database)
        response.setTotalCost(booking.getTotalCost());

        // Map booking status (e.g., PENDING, ACTIVE, COMPLETED)
        response.setStatus(booking.getStatus());

        // Map user-related details
        // Extracts basic user info from associated user entity
        response.setUserId(booking.getUser().getId());
        response.setUserName(booking.getUser().getName());

        // Map creation timestamp
        // Formatting is handled at DTO level (e.g., using @JsonFormat)
        response.setCreatedAt(booking.getCreatedAt());

        // Return the fully mapped response object
        return response;
    }
}