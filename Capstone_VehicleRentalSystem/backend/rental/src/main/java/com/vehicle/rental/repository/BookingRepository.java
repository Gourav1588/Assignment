package com.vehicle.rental.repository;

import com.vehicle.rental.entity.Booking;
import com.vehicle.rental.entity.Booking.BookingStatus;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;
import java.util.List;

@Repository
public interface BookingRepository extends JpaRepository<Booking, Long> {

    // Fetch bookings for a specific user
    // Used to display booking history for logged-in users
    // Supports pagination for large datasets
    Page<Booking> findByUserId(Long userId, Pageable pageable);

    // Fetch bookings based on status (e.g., ACTIVE, PENDING, COMPLETED)
    // Typically used in admin dashboards for filtering bookings
    Page<Booking> findByStatus(BookingStatus status, Pageable pageable);

    // Check if a vehicle has any bookings with given statuses
    // Used before soft deleting a vehicle to prevent conflicts
    boolean existsByVehicleIdAndStatusIn(
            Long vehicleId,
            List<BookingStatus> statuses
    );

    // Check whether a vehicle is available for a given date range
    // Core logic to prevent overlapping bookings
    // Considers only PENDING and ACTIVE bookings
    // Returns true if no conflicting booking exists, otherwise false
    @Query("""
        SELECT COUNT(b) = 0 
        FROM Booking b 
        WHERE b.vehicle.id = :vehicleId 
        AND b.status IN ('PENDING', 'ACTIVE') 
        AND b.startDate <= :endDate 
        AND b.endDate >= :startDate
        """)
    boolean isVehicleAvailable(
            @Param("vehicleId") Long vehicleId,
            @Param("startDate") LocalDate startDate,
            @Param("endDate") LocalDate endDate
    );
}