package com.training.todoapp.service;

import com.training.todoapp.client.NotificationServiceClient;
import com.training.todoapp.dto.TodoDTO;
import com.training.todoapp.entity.Todo;
import com.training.todoapp.entity.Todo.Status;
import com.training.todoapp.exception.TodoNotFoundException;
import com.training.todoapp.repository.TodoRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.List;
import java.util.Optional;

import static org.assertj.core.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

// I use MockitoExtension so we can mock dependencies without loading the database.
@ExtendWith(MockitoExtension.class)
class TodoServiceTest {

    @Mock TodoRepository todoRepository;
    @Mock NotificationServiceClient notificationClient;
    @InjectMocks TodoService todoService;

    private Todo pendingTodo;

    @BeforeEach
    void setUp() throws Exception {
        pendingTodo = new Todo("Buy groceries", "Milk and eggs", Status.PENDING);
        // Using reflection to inject the ID privately for testing.
        setId(pendingTodo, 1L);
    }

    // create

    @Test
    void createTodo_savesAndReturnsDto() {
        when(todoRepository.save(any())).thenReturn(pendingTodo);

        TodoDTO result = todoService.createTodo(buildDto("Buy groceries", null, null));

        assertThat(result.getTitle()).isEqualTo("Buy groceries");
        assertThat(result.getStatus()).isEqualTo(Status.PENDING);
        verify(notificationClient).onTodoCreated(1L, "Buy groceries");
    }

    // getAll

    @Test
    void getAllTodos_returnsAllMappedDtos() {
        when(todoRepository.findAll()).thenReturn(List.of(pendingTodo));

        List<TodoDTO> result = todoService.getAllTodos();

        assertThat(result).hasSize(1);
        assertThat(result.get(0).getTitle()).isEqualTo("Buy groceries");
    }

    @Test
    void getAllTodos_whenEmpty_returnsEmptyList() {
        when(todoRepository.findAll()).thenReturn(List.of());
        assertThat(todoService.getAllTodos()).isEmpty();
    }

    // getById

    @Test
    void getTodoById_whenFound_returnsDto() {
        when(todoRepository.findById(1L)).thenReturn(Optional.of(pendingTodo));

        TodoDTO result = todoService.getTodoById(1L);

        assertThat(result.getId()).isEqualTo(1L);
    }

    @Test
    void getTodoById_whenNotFound_throwsException() {
        when(todoRepository.findById(5L)).thenReturn(Optional.empty());

        assertThatThrownBy(() -> todoService.getTodoById(5L))
                .isInstanceOf(TodoNotFoundException.class)
                .hasMessageContaining("5");
    }

    // update

    @Test
    void updateTodo_changesTitle_doesNotNotify() {
        when(todoRepository.findById(1L)).thenReturn(Optional.of(pendingTodo));
        when(todoRepository.save(any())).thenAnswer(inv -> inv.getArgument(0));

        todoService.updateTodo(1L, buildDto("New title", null, null));

        // I specifically verify that no interaction happens to prove we aren't spamming events.
        verifyNoInteractions(notificationClient);
    }

    @Test
    void updateTodo_statusChange_notifiesDownstream() {
        when(todoRepository.findById(1L)).thenReturn(Optional.of(pendingTodo));
        when(todoRepository.save(any())).thenAnswer(inv -> inv.getArgument(0));

        todoService.updateTodo(1L, buildDto(null, null, Status.COMPLETED));

        verify(notificationClient).onTodoStatusChanged(1L, "PENDING", "COMPLETED");
    }

    @Test
    void updateTodo_sameStatus_throwsIllegalArgumentException() {
        when(todoRepository.findById(1L)).thenReturn(Optional.of(pendingTodo));

        assertThatThrownBy(() -> todoService.updateTodo(1L, buildDto(null, null, Status.PENDING)))
                .isInstanceOf(IllegalArgumentException.class);

        verify(todoRepository, never()).save(any());
    }

    @Test
    void updateTodo_whenNotFound_throwsException() {
        when(todoRepository.findById(9L)).thenReturn(Optional.empty());

        assertThatThrownBy(() -> todoService.updateTodo(9L, buildDto("x", null, null)))
                .isInstanceOf(TodoNotFoundException.class);
    }

    // delete

    @Test
    void deleteTodo_deletesAndNotifies() {
        when(todoRepository.findById(1L)).thenReturn(Optional.of(pendingTodo));

        // I updated this test to expect no return value (void) due to the RESTful standard update.
        todoService.deleteTodo(1L);

        verify(todoRepository).delete(pendingTodo);
        verify(notificationClient).onTodoDeleted(1L);
    }

    @Test
    void deleteTodo_whenNotFound_throwsException() {
        when(todoRepository.findById(8L)).thenReturn(Optional.empty());

        assertThatThrownBy(() -> todoService.deleteTodo(8L))
                .isInstanceOf(TodoNotFoundException.class);

        verify(todoRepository, never()).delete(any());
    }

    // helpers

    private TodoDTO buildDto(String title, String description, Status status) {
        TodoDTO dto = new TodoDTO();
        dto.setTitle(title);
        dto.setDescription(description);
        dto.setStatus(status);
        return dto;
    }

    private void setId(Todo todo, Long id) throws Exception {
        var field = Todo.class.getDeclaredField("id");
        field.setAccessible(true);
        field.set(todo, id);
    }
}