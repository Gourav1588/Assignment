package com.vehicle.rental.mapper;

import com.vehicle.rental.dto.response.BookingResponse;
import com.vehicle.rental.entity.Booking;
import com.vehicle.rental.entity.User;
import com.vehicle.rental.entity.Vehicle;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Unit tests for the BookingMapper.
 * Covers nested object flattening, time-based business logic, and dynamic status resolution.
 */
class BookingMapperTest {

    private BookingMapper bookingMapper;

    @BeforeEach
    void setUp() {
        bookingMapper = new BookingMapper();
    }

    /**
     * Helper method to create a fully populated dummy booking for testing.
     */
    private Booking createDummyBooking() {
        User user = new User();
        user.setId(100L);
        user.setName("Alice Smith");

        Vehicle vehicle = new Vehicle();
        vehicle.setId(200L);
        vehicle.setName("Royal Enfield");
        vehicle.setType(Vehicle.VehicleType.BIKE);
        vehicle.setPricePerDay(800.0);

        Booking booking = new Booking();
        booking.setId(50L);
        booking.setUser(user);
        booking.setVehicle(vehicle);
        booking.setTotalCost(1600.0);
        booking.setCreatedAt(LocalDateTime.now().minusDays(1));

        return booking;
    }

    /**
     * Tests standard mapping and ensures that total hours are calculated correctly.
     */
    @Test
    void shouldFlattenNestedObjectsAndCalculateHours() {
        // Given
        Booking booking = createDummyBooking();
        booking.setStatus(Booking.BookingStatus.PENDING);
        // Set trip for exactly 48 hours
        booking.setStartTime(LocalDateTime.now().plusDays(1));
        booking.setEndTime(LocalDateTime.now().plusDays(3));

        // When
        BookingResponse response = bookingMapper.toResponse(booking);

        // Then
        assertNotNull(response);
        assertEquals(50L, response.getId());
        assertEquals("Alice Smith", response.getUserName());
        assertEquals("Royal Enfield", response.getVehicleName());
        assertEquals("BIKE", response.getVehicleType());
        assertEquals(48L, response.getTotalHours(), "Hours should be calculated based on start and end time");
        assertEquals(Booking.BookingStatus.PENDING, response.getStatus());
    }

    /**
     * Tests the fallback logic that forces total hours to be at least 1,
     * even if the booking duration is under an hour.
     */
    @Test
    void shouldEnforceMinimumOneHourDuration() {
        // Given
        Booking booking = createDummyBooking();
        booking.setStatus(Booking.BookingStatus.COMPLETED);

        LocalDateTime now = LocalDateTime.now();
        booking.setStartTime(now);
        booking.setEndTime(now.plusMinutes(30)); // Only 30 mins

        // When
        BookingResponse response = bookingMapper.toResponse(booking);

        // Then
        assertEquals(1L, response.getTotalHours(), "Durations under 1 hour should default to 1 hour");
    }

    /**
     * Tests the dynamic status resolution:
     * If the status is ACTIVE but the current time has passed the end time,
     * it should automatically display as COMPLETED to the client.
     */
    @Test
    void shouldDynamicallyResolveOverdueActiveBookingAsCompleted() {
        // Given
        Booking booking = createDummyBooking();
        booking.setStatus(Booking.BookingStatus.ACTIVE);

        // The trip ended 2 hours ago
        booking.setStartTime(LocalDateTime.now().minusHours(10));
        booking.setEndTime(LocalDateTime.now().minusHours(2));

        // When
        BookingResponse response = bookingMapper.toResponse(booking);

        // Then
        assertEquals(Booking.BookingStatus.COMPLETED, response.getStatus(),
                "An active booking whose end time has passed should resolve to COMPLETED");
    }

    /**
     * Ensures an ACTIVE booking that has not yet reached its end time
     * remains ACTIVE.
     */
    @Test
    void shouldKeepStatusActiveIfEndTimeIsInFuture() {
        // Given
        Booking booking = createDummyBooking();
        booking.setStatus(Booking.BookingStatus.ACTIVE);

        // The trip started yesterday and ends tomorrow
        booking.setStartTime(LocalDateTime.now().minusDays(1));
        booking.setEndTime(LocalDateTime.now().plusDays(1));

        // When
        BookingResponse response = bookingMapper.toResponse(booking);

        // Then
        assertEquals(Booking.BookingStatus.ACTIVE, response.getStatus());
    }
}