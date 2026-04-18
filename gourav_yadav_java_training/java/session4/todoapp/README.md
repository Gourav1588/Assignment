# Todo App — Enterprise Flow & Testing

A Spring Boot REST API for managing todo tasks, built as part of the enterprise flow and testing session.

---

## Tech Stack

| | |
|---|---|
| Java | 17 |
| Spring Boot | 3.x |
| Database | H2 (in-memory) |
| Build Tool | Maven |
| Testing | JUnit 5, Mockito, AssertJ |
| Logging | SLF4J (Logback) |

---

## Running the App

```

App starts at `http://localhost:8080`  
No database setup needed — H2 runs in memory automatically.

```bash
./mvnw test        # run all tests
```

---

## Project Structure

```
src/
├── main/java/com/training/todoapp/
│   ├── controller/
│   │   └── TodoController.java
│   ├── service/
│   │   └── TodoService.java
│   ├── client/
│   │   └── NotificationServiceClient.java
│   ├── repository/
│   │   └── TodoRepository.java
│   ├── dto/
│   │   └── TodoDTO.java
│   ├── entity/
│   │   └── Todo.java
│   └── exception/
│       ├── GlobalExceptionHandler.java
│       └── TodoNotFoundException.java
│
└── test/java/com/training/todoapp/
    ├── controller/
    │   └── TodoControllerTest.java
    └── service/
        └── TodoServiceTest.java
```

---

## API Endpoints

| Method | Endpoint | Description | Status |
|---|---|---|---|
| POST | `/todos` | Create a todo | 201 |
| GET | `/todos` | Get all todos | 200 |
| GET | `/todos/{id}` | Get todo by id | 200 |
| PUT | `/todos/{id}` | Full update | 200 |
| PATCH | `/todos/{id}` | Partial update | 200 |
| DELETE | `/todos/{id}` | Delete a todo | 204 |

---

## Request & Response

### Create Todo

```json
POST /todos
{
  "title": "Buy groceries",
  "description": "Milk and eggs"
}
```

`status` is optional — defaults to `PENDING` if not provided.

### Response

```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk and eggs",
  "status": "PENDING",
  "createdAt": "2026-04-18T10:30:00"
}
```

### Status values

`PENDING` `COMPLETED`

---

## Validation Rules

| Field | Rule |
|---|---|
| `title` | Required, cannot be blank, minimum 3 characters |
| `status` | Must be `PENDING` or `COMPLETED` |

Transitioning a todo to its **current status** returns `400`.

---

## Error Responses

All errors return `{ "error": "..." }`.  
Validation errors return `{ "fieldName": "message" }`.

| Scenario | Status |
|---|---|
| Todo not found | 404 |
| Validation failure | 400 |
| Same-status transition | 400 |
| Invalid status value | 400 |
| Invalid path variable type | 400 |
| Unexpected error | 500 |

---

## Architecture

```
Controller  →  Service  →  Repository
                  ↓
          NotificationServiceClient
```

- All dependencies use **constructor injection only**
- No business logic in controllers
- Entities never exposed directly — all responses go through DTOs
- Exceptions thrown in service layer, caught by `GlobalExceptionHandler`

---

## Logging

SLF4J used across all layers.

| Layer | What gets logged |
|---|---|
| Controller | Every incoming request (method + path) |
| Service | Lifecycle events — create, update, delete, not found |
| NotificationServiceClient | Outbound event dispatch |

To enable debug logs:

```properties
# src/main/resources/application.properties
logging.level.com.training.todoapp=DEBUG
```

---

## NotificationServiceClient

Lives in the `client/` package — separated from `service/` because it is an outbound adapter, not business logic.

Fires on three events:
- Todo created → `onTodoCreated()`
- Todo status changed → `onTodoStatusChanged()`
- Todo deleted → `onTodoDeleted()`



---

## Tests

| Class | Coverage |
|---|---|
| `TodoServiceTest` | All CRUD paths, exception scenarios, notification call verification |
| `TodoControllerTest` | All endpoints via MockMvc, validation edge cases, error response shapes |

Target coverage: **85%+**

All test dependencies come from `spring-boot-starter-test` — no extra setup needed.