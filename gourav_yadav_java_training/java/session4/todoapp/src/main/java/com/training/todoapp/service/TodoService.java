package com.training.todoapp.service;

import com.training.todoapp.client.NotificationServiceClient;
import com.training.todoapp.dto.TodoDTO;
import com.training.todoapp.entity.Todo;
import com.training.todoapp.entity.Todo.Status;
import com.training.todoapp.exception.TodoNotFoundException;
import com.training.todoapp.repository.TodoRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

// I'm marking this with @Service to hold all the core business logic and data mapping.
@Service
public class TodoService {

    private static final Logger log = LoggerFactory.getLogger(TodoService.class);

    private final TodoRepository todoRepository;
    private final NotificationServiceClient notificationClient;

    // I'm using constructor injection for dependencies.
    public TodoService(TodoRepository todoRepository,
                       NotificationServiceClient notificationClient) {
        this.todoRepository = todoRepository;
        this.notificationClient = notificationClient;
    }

    public TodoDTO createTodo(TodoDTO dto) {
        log.debug("Creating todo, title='{}'", dto.getTitle());

        Todo saved = todoRepository.save(
                new Todo(dto.getTitle(), dto.getDescription(), dto.getStatus())
        );

        log.info("Todo created [id={}]", saved.getId());

        // I'm firing the simulated event only after a successful database save.
        notificationClient.onTodoCreated(saved.getId(), saved.getTitle());

        return toDTO(saved);
    }

    public List<TodoDTO> getAllTodos() {
        log.debug("Fetching all todos");
        return todoRepository.findAll()
                .stream()
                .map(this::toDTO)
                .collect(Collectors.toList());
    }

    public TodoDTO getTodoById(Long id) {
        log.debug("Fetching todo [id={}]", id);
        return toDTO(findOrThrow(id));
    }

    public TodoDTO updateTodo(Long id, TodoDTO dto) {
        log.debug("Updating todo [id={}]", id);

        Todo todo = findOrThrow(id);

        if (dto.getStatus() != null) {
            // I strictly enforce state transitions to prevent redundant database calls.
            if (todo.getStatus() == dto.getStatus()) {
                throw new IllegalArgumentException(
                        "Status is already " + dto.getStatus() + " — no transition needed");
            }
            String previous = todo.getStatus().name();
            todo.setStatus(dto.getStatus());
            notificationClient.onTodoStatusChanged(id, previous, dto.getStatus().name());
        }

        if (dto.getTitle() != null)       todo.setTitle(dto.getTitle());
        if (dto.getDescription() != null) todo.setDescription(dto.getDescription());

        Todo updated = todoRepository.save(todo);
        log.info("Todo updated [id={}]", id);

        return toDTO(updated);
    }

    // I've changed this to void to follow RESTful semantics for the DELETE endpoint.
    public void deleteTodo(Long id) {
        log.debug("Deleting todo [id={}]", id);

        todoRepository.delete(findOrThrow(id));
        notificationClient.onTodoDeleted(id);

        log.info("Todo deleted [id={}]", id);
    }

    // -------------------------------------------------------------------------

    // I use this private helper to centralize the 404 Exception logic.
    private Todo findOrThrow(Long id) {
        return todoRepository.findById(id)
                .orElseThrow(() -> {
                    log.warn("Todo not found [id={}]", id);
                    return new TodoNotFoundException("Todo not found with id: " + id);
                });
    }

    // I manually map Entity to DTO here to prevent exposing internal database fields to the user.
    private TodoDTO toDTO(Todo todo) {
        TodoDTO dto = new TodoDTO();
        dto.setId(todo.getId());
        dto.setTitle(todo.getTitle());
        dto.setDescription(todo.getDescription());
        dto.setStatus(todo.getStatus());
        dto.setCreatedAt(todo.getCreatedAt());
        return dto;
    }
}