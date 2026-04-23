package com.vehicle.rental.dto.response;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.vehicle.rental.entity.Booking.BookingStatus;
import lombok.Data;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Data
public class BookingResponse {

    private Long id;

    // vehicle details
    private Long vehicleId;
    private String vehicleName;
    private String vehicleType;
    private Double pricePerDay;

    // booking details
    private LocalDate startDate;
    private LocalDate endDate;
    private Long totalDays;
    private Double totalCost;
    private BookingStatus status;

    // user details
    private Long userId;
    private String userName;

    @JsonFormat(pattern = "dd-MM-yyyy HH:mm:ss")
    private LocalDateTime createdAt;
}