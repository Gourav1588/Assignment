package com.vehicle.rental.repository;

import com.vehicle.rental.entity.Booking;
import com.vehicle.rental.entity.Booking.BookingStatus;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime; //
import java.util.List;

/**
 * Data Access Object for Booking entities.
 * Handles complex date-range queries to ensure vehicles are not double-booked.
 */
@Repository
public interface BookingRepository extends JpaRepository<Booking, Long> {

    Page<Booking> findByUserId(Long userId, Pageable pageable);

    Page<Booking> findByStatus(BookingStatus status, Pageable pageable);

    boolean existsByVehicleIdAndStatusIn(Long vehicleId, List<BookingStatus> statuses);

    /* =========================================================================
       TIME-BASED OVERLAP QUERY
       ========================================================================= */
    /**
     * Checks if a vehicle is completely free during a specific exact-time range.
     * Uses exclusive bounds (< and >) to allow back-to-back same-day bookings.
     */
    @Query("""
        SELECT COUNT(b) = 0 
        FROM Booking b 
        WHERE b.vehicle.id = :vehicleId 
        AND b.status IN ('PENDING', 'ACTIVE') 
        AND b.startTime < :endTime 
        AND b.endTime > :startTime
        """)
    boolean isVehicleAvailable(
            @Param("vehicleId") Long vehicleId,
            @Param("startTime") LocalDateTime startTime,
            @Param("endTime") LocalDateTime endTime
    );

    /**
     * Verifies if a vehicle has any ongoing or upcoming trips.
     * Used as a safeguard before allowing a vehicle to be soft-deleted or deactivated.
     */
    @Query("SELECT COUNT(b) > 0 FROM Booking b WHERE b.vehicle.id = :vehicleId " +
            "AND b.status IN ('ACTIVE',  'PENDING') " +
            "AND b.endTime >= CURRENT_TIMESTAMP")
    boolean existsActiveOrFutureBookingsForVehicle(@Param("vehicleId") Long vehicleId);
}