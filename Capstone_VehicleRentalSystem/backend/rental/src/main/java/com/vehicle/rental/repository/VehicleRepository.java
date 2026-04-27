package com.vehicle.rental.repository;

import com.vehicle.rental.entity.Vehicle;
import com.vehicle.rental.entity.Vehicle.VehicleType;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;

@Repository
public interface VehicleRepository extends JpaRepository<Vehicle, Long> {

    // Fetch vehicles with dynamic filtering
    // Supports optional filters like name, type, and category
    // If any parameter is null, that filter is ignored automatically
    // Only active vehicles are returned
    @Query("SELECT v FROM Vehicle v WHERE " +
            "(:name = '' OR LOWER(v.name) LIKE LOWER(CONCAT('%', :name, '%'))) AND " +
            "(:type IS NULL OR v.type = :type) AND " +
            "(:categoryId IS NULL OR v.category.id = :categoryId)")
    Page<Vehicle> findAllWithFilters(
            @Param("name") String name,
            @Param("type") VehicleType type,
            @Param("categoryId") Long categoryId,
            Pageable pageable);

    // Check if a vehicle exists and is currently active
    // Commonly used before performing operations like soft delete
    boolean existsByIdAndIsActiveTrue(Long id);

    boolean existsByNameIgnoreCase(String name);

    boolean existsByRegistrationNumberIgnoreCase(String registrationNumber);


}