package com.vehicle.rental.mapper;

import com.vehicle.rental.dto.response.BookingResponse;
import com.vehicle.rental.entity.Booking;
import org.springframework.stereotype.Component;

import java.time.temporal.ChronoUnit;

/**
 * Mapper component for translating Booking entities into BookingResponse DTOs.
 */
@Component
public class BookingMapper {

    /**
     * Transforms complex nested Booking entity data into a flattened, client-friendly format.
     * * @param booking The source Booking entity.
     * @return The formatted BookingResponse DTO.
     */
    public BookingResponse toResponse(Booking booking) {
        BookingResponse response = new BookingResponse();

        response.setId(booking.getId());

        // Flatten vehicle relationships
        response.setVehicleId(booking.getVehicle().getId());
        response.setVehicleName(booking.getVehicle().getName());
        response.setVehicleType(booking.getVehicle().getType().name());
        response.setPricePerDay(booking.getVehicle().getPricePerDay());

        response.setStartDate(booking.getStartDate());
        response.setEndDate(booking.getEndDate());

        // Calculate total inclusive days
        long days = ChronoUnit.DAYS.between(booking.getStartDate(), booking.getEndDate()) + 1;
        response.setTotalDays(days);

        response.setTotalCost(booking.getTotalCost());
        response.setStatus(booking.getStatus());

        // Flatten user relationships
        response.setUserId(booking.getUser().getId());
        response.setUserName(booking.getUser().getName());

        response.setCreatedAt(booking.getCreatedAt());

        return response;
    }
}