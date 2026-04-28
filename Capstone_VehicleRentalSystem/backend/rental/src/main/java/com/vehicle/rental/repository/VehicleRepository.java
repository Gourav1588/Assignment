package com.vehicle.rental.repository;

import com.vehicle.rental.entity.Vehicle;
import com.vehicle.rental.entity.Vehicle.VehicleType;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

/**
 * Data Access Object for Vehicle entities.
 * Includes dynamic filtering logic to power the frontend catalog search.
 */
@Repository
public interface VehicleRepository extends JpaRepository<Vehicle, Long> {

    /**
     * Dynamically filters the fleet based on user input.
     * If a parameter is null or empty, that specific filter is automatically bypassed.
     */
    @Query("SELECT v FROM Vehicle v WHERE " +
            "(:name = '' OR LOWER(v.name) LIKE LOWER(CONCAT('%', :name, '%'))) AND " +
            "(:type IS NULL OR v.type = :type) AND " +
            "(:categoryId IS NULL OR v.category.id = :categoryId)")
    Page<Vehicle> findAllWithFilters(
            @Param("name") String name,
            @Param("type") VehicleType type,
            @Param("categoryId") Long categoryId,
            Pageable pageable);

    boolean existsByIdAndIsActiveTrue(Long id);

    boolean existsByNameIgnoreCase(String name);

    boolean existsByRegistrationNumberIgnoreCase(String registrationNumber);
}