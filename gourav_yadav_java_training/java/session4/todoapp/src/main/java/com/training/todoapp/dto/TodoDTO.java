package com.training.todoapp.dto;

import com.training.todoapp.entity.Todo.Status;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

public class TodoDTO {

    // DTO controls input data and prevents direct exposure of entity

    private Long id;

    @NotNull(message = "Title cannot be null")
    @Size(min = 3, message = "Title must be at least 3 characters")
    private String title;

    private String description;


    private Status status;// Optional → defaults to PENDING in backend

    public TodoDTO() {}

    // Getters & Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }

    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }

    public Status getStatus() { return status; }
    public void setStatus(Status status) { this.status = status; }
}