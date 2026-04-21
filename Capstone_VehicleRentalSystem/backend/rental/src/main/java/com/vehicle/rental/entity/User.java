package com.vehicle.rental.entity;

import com.fasterxml.jackson.annotation.JsonIgnore;
import jakarta.persistence.*;
import lombok.Data;
import java.time.LocalDateTime;

// I used Lombok's @Data to keep this file clean. I don't want to clutter
// my core database entity with dozens of lines of boilerplate getters and setters.
@Data
// I specifically set the table name to "users" because "user" is a reserved
// keyword in PostgreSQL. Doing this prevents unexpected SQL syntax errors
// when Hibernate tries to auto-generate our tables.
@Entity
@Table(name = "users")
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;

    // I made the email strictly unique at the database level because
    // I am using it as the primary identifier for our JWT login process.
    // This stops duplicate accounts right at the data layer.
    @Column(nullable = false, unique = true)
    private String email;

    // I added @JsonIgnore here as a strict security failsafe. Even though I plan
    // to use DTOs to format API responses, if this raw entity ever accidentally
    // leaks out through a controller, Jackson will completely drop the hashed
    // password before converting it to JSON.
    @JsonIgnore
    @Column(nullable = false)
    private String password;

    // I'm using EnumType.STRING instead of the default ordinal (numeric) type.
    // If I just used numbers and later added a "MANAGER" role in the middle of the enum,
    // it would completely corrupt the existing database records. Saving it as raw text
    // makes the database much safer and easier to read.
    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private Role role = Role.USER;

    // I set this to default to the exact moment the object is instantiated.
    // It's a simple way to maintain an audit trail of when accounts are created.
    @Column(name = "created_at")
    private LocalDateTime createdAt = LocalDateTime.now();

    public enum Role {
        USER, ADMIN
    }
}