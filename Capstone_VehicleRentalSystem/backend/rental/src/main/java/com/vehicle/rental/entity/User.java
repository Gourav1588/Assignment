package com.vehicle.rental.entity;

import com.fasterxml.jackson.annotation.JsonIgnore;
import jakarta.persistence.*;
import lombok.Data;

import java.time.LocalDateTime;

/**
 * JPA Entity representing a registered user in the system.
 * Maps to the "users" table to avoid conflicts with PostgreSQL reserved keywords.
 * Manages core identity, authentication credentials, and authorization roles.
 */
@Data
@Entity
@Table(name = "users")
public class User {

    /**
     * The unique primary key for the user record.
     */
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    /**
     * The display name of the user.
     */
    @Column(nullable = false)
    private String name;

    /**
     * The user's email address.
     * Enforced as strictly unique at the database level, as it serves as the
     * primary identifier for JWT authentication and login.
     */
    @Column(nullable = false, unique = true)
    private String email;

    /**
     * The securely hashed password.
     * Annotated with @JsonIgnore as a strict security failsafe to ensure the
     * hash is never accidentally serialized and leaked in an API response.
     */
    @JsonIgnore
    @Column(nullable = false)
    private String password;

    /**
     * The authorization tier of the user (e.g., USER, ADMIN).
     * Stored as a plain string (EnumType.STRING) rather than a numeric ordinal
     * to prevent database corruption if new roles are added to the enum later.
     */
    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private Role role = Role.USER;

    /**
     * The exact timestamp when the user account was created.
     * Provides a foundational audit trail for account generation.
     */
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt = LocalDateTime.now();

    /**
     * Enumeration of system-recognized authorization roles.
     */
    public enum Role {
        /** Standard customer with booking privileges. */
        USER,
        /** Administrator with full system and fleet management capabilities. */
        ADMIN
    }
}