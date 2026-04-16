package com.training.todoapp.entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "todos")
public class Todo {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id; // Primary key (auto-generated)

    @Column(nullable = false)
    private String title; // Task title (required)

    @Column
    private String description;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private Status status; // Stores enum as String (PENDING/COMPLETED)

    @Column(nullable = false)
    private LocalDateTime createdAt;

    public enum Status {
        PENDING,
        COMPLETED
    }

    // Default constructor → sets default values automatically
    public Todo() {
        this.status = Status.PENDING;
        this.createdAt = LocalDateTime.now();
    }

    // Uses provided values, but applies default status if null
    public Todo(String title, String description, Status status) {
        this.title = title;
        this.description = description;
        this.status = (status != null) ? status : Status.PENDING;
        this.createdAt = LocalDateTime.now();
    }

    // Getters & Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }

    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }

    public Status getStatus() { return status; }
    public void setStatus(Status status) { this.status = status; }

    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
}