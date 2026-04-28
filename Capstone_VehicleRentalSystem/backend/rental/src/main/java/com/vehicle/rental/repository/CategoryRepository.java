package com.vehicle.rental.repository;

import com.vehicle.rental.entity.VehicleCategory;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface CategoryRepository extends JpaRepository<VehicleCategory, Long> {

    boolean existsByName(String name);

    Optional<VehicleCategory> findByName(String name);

    Optional<VehicleCategory> findByNameIgnoreCase(String name);
}