package com.training.todoapp.service;

import com.training.todoapp.dto.TodoDTO;
import com.training.todoapp.entity.Todo;
import com.training.todoapp.exception.TodoNotFoundException;
import com.training.todoapp.repository.TodoRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class TodoService {

    private final TodoRepository todoRepository;

    // Service layer handles business logic and DTO ↔ Entity conversion
    public TodoService(TodoRepository todoRepository) {
        this.todoRepository = todoRepository;
    }

    // CREATE
    public TodoDTO createTodo(TodoDTO dto) {
        Todo todo = new Todo();
        todo.setTitle(dto.getTitle());
        todo.setDescription(dto.getDescription());
        todo.setStatus(dto.getStatus() != null ? dto.getStatus() : Todo.Status.PENDING);

        Todo saved = todoRepository.save(todo);
        return convertToDTO(saved);
    }

    // GET ALL
    public List<TodoDTO> getAllTodos() {
        return todoRepository.findAll()
                .stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
    }

    // GET BY ID
    public TodoDTO getTodoById(Long id) {
        Todo todo = todoRepository.findById(id)
                .orElseThrow(() -> new TodoNotFoundException("Todo not found with id: " + id));
        return convertToDTO(todo);
    }

    // UPDATE
    public TodoDTO updateTodo(Long id, TodoDTO dto) {
        Todo todo = todoRepository.findById(id)
                .orElseThrow(() -> new TodoNotFoundException("Todo not found with id: " + id));

        // Validate allowed status transitions
        if (dto.getStatus() != null && !dto.getStatus().equals(todo.getStatus())) {
            if ((todo.getStatus() == Todo.Status.PENDING && dto.getStatus() == Todo.Status.COMPLETED) ||
                    (todo.getStatus() == Todo.Status.COMPLETED && dto.getStatus() == Todo.Status.PENDING)) {
                todo.setStatus(dto.getStatus());
            } else {
                throw new IllegalArgumentException("Invalid status transition");
            }
        }

        if (dto.getTitle() != null) todo.setTitle(dto.getTitle());
        if (dto.getDescription() != null) todo.setDescription(dto.getDescription());

        Todo updated = todoRepository.save(todo);
        return convertToDTO(updated);
    }

    // DELETE
    public String deleteTodo(Long id) {
        Todo todo = todoRepository.findById(id)
                .orElseThrow(() -> new TodoNotFoundException("Todo not found with id: " + id));
        todoRepository.delete(todo);
        return "Todo with id " + id + " deleted successfully";
    }

    // Convert Entity → DTO to control response data
    private TodoDTO convertToDTO(Todo todo) {
        TodoDTO dto = new TodoDTO();
        dto.setId(todo.getId());
        dto.setTitle(todo.getTitle());
        dto.setDescription(todo.getDescription());
        dto.setStatus(todo.getStatus());
        return dto;
    }
}