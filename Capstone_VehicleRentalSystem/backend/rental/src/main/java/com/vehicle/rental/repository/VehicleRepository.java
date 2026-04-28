package com.vehicle.rental.repository;

import com.vehicle.rental.entity.Vehicle;
import com.vehicle.rental.entity.Vehicle.VehicleType;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

/* =========================================================================
   VEHICLE REPOSITORY
   Data Access Object for Fleet Inventory. Handles dynamic search filtering
   and operational status separation.
   ========================================================================= */
@Repository
public interface VehicleRepository extends JpaRepository<Vehicle, Long> {

    /* =========================================================================
       1. PUBLIC QUERIES (RESTRICTED DATA)
       ========================================================================= */

    /**
     * Dynamically filters the fleet for the Public User Catalog.
     * CRITICAL: Enforces 'isActive = true' so users never see retired vehicles.
     */
    @Query("SELECT v FROM Vehicle v WHERE v.isActive = true AND " +
            "(:name = '' OR LOWER(v.name) LIKE LOWER(CONCAT('%', :name, '%'))) AND " +
            "(:type IS NULL OR v.type = :type) AND " +
            "(:categoryId IS NULL OR v.category.id = :categoryId)")
    Page<Vehicle> findAllActiveWithFilters(
            @Param("name") String name,
            @Param("type") VehicleType type,
            @Param("categoryId") Long categoryId,
            Pageable pageable);


    /* =========================================================================
       2. ADMIN QUERIES (UNRESTRICTED DATA)
       ========================================================================= */

    /**
     * Dynamically filters the entire fleet for the Admin Dashboard.
     * Bypasses the 'isActive' check to show both Operational and Retired vehicles.
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


    /* =========================================================================
       3. VALIDATION UTILITIES
       ========================================================================= */

    boolean existsByIdAndIsActiveTrue(Long id);

    boolean existsByNameIgnoreCase(String name);

    boolean existsByRegistrationNumberIgnoreCase(String registrationNumber);
}