package com.vehicle.rental.repository;

import com.vehicle.rental.entity.VehicleCategory;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface CategoryRepository extends JpaRepository<VehicleCategory, Long> {

    // Check if a category with the given name already exists
    // Used to prevent duplicate category creation or updates
    boolean existsByName(String name);

    // Retrieve a category based on its name
    // Returns Optional to safely handle cases where category may not exist
    Optional<VehicleCategory> findByName(String name);

}