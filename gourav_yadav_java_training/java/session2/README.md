# Java Training - Session 2 (Spring Boot Assignment)



---


## Overview
This project is developed as part of Session 2 of the Java training assignment.  
It implements a Spring Boot REST API to demonstrate core concepts such as layered architecture, dependency injection, and component-based design.

The application follows clean coding practices with proper separation of concerns.  
It uses in-memory data storage instead of a database, as required in the assignment.

---

## Architecture

The project strictly follows a clean layered architecture:

Controller -> Service -> Repository
Controller -> Service -> Component

* **Controller** - Handles incoming HTTP requests only
* **Service** - Contains all business logic
* **Repository** - Manages in-memory data operations
* **Component** - Reusable helper logic used by services

---

## Key Design Principles

* Constructor injection used throughout, no field or setter injection
* Business logic stays in Service layer only
* Controller never talks to Repository directly
* Loose coupling achieved using interfaces and components
* Global exception handling using `@RestControllerAdvice`

---

## Systems Implemented

### 1. User Management System

Manages a list of users stored in memory using ArrayList.
Supports fetching all users, fetching by id, and creating new users.
Auto-increments user id using a counter in the repository.

---

### 2. Notification System

Triggers a notification message when the API is called.
Service delegates message generation to `NotificationComponent`
to follow separation of concerns.

---

### 3. Dynamic Message Formatter System

Returns different messages based on the type passed in the request.
Uses a `MessageFormatter` interface implemented by two components.
Service selects the correct formatter at runtime using a Map.
No if-else .

---

## API Endpoints

### User Management

| Method | Endpoint    | Description       |
| ------ | ----------- | ----------------- |
| GET    | /users      | Fetch all users   |
| GET    | /users/{id} | Fetch user by id  |
| POST   | /users      | Create a new user |

---

### Notification

| Method | Endpoint | Description            |
| ------ | -------- | ---------------------- |
| POST   | /notify  | Trigger a notification |

---

### Message Formatter

| Method | Endpoint            | Description       |
| ------ | ------------------- | ----------------- |
| GET    | /message?type=SHORT | Get short message |
| GET    | /message?type=LONG  | Get long message  |

---

## Exception Handling

Global exception handling is implemented using `@RestControllerAdvice`.
All exceptions are handled centrally instead of in individual controllers.

| Exception                 | HTTP Status | When Thrown                  |
| ------------------------- | ----------- | ---------------------------- |
| ResourceNotFoundException | 404         | User not found by id         |
| IllegalArgumentException  | 400         | Invalid message type passed  |
| RuntimeException          | 500         | Unexpected server-side error |

---

## Technologies Used

* Java 17
* Spring Boot
* Maven
* REST APIs

---

## Spring Concepts Demonstrated

* IoC (Inversion of Control) - Spring manages object lifecycle
* Dependency Injection - Constructor-based injection
* Component Scanning - Auto detection of beans via annotations

### Annotations Used

* `@RestController`
* `@Service`
* `@Repository`
* `@Component`
* `@RestControllerAdvice`

---

## How To Run

### Prerequisites

* Java 17
* Maven

### Steps

```bash
# Clone repository
git clone https://github.com/Gourav1588/Assignment.git

# Navigate to session2 project
cd gourav_yadav_java_training/java/session2

# Run the application
mvn spring-boot:run
```

---

## Application URL

http://localhost:8080

---

## Sample Requests

### Fetch All Users

GET http://localhost:8080/users

### Fetch User By Id

GET http://localhost:8080/users/1

### Create New User

POST http://localhost:8080/users
Content-Type: application/json

```json
{
  "name": "Gourav",
  "email": "gourav@gmail.com"
}
```

---

### Trigger Notification

POST http://localhost:8080/notify

---

### Get Short Message

GET http://localhost:8080/message?type=SHORT

### Get Long Message

GET http://localhost:8080/message?type=LONG

---

## Project Structure

```
gourav_yadav_java_training/
 ├── java/
 │    └── session2/
 │         └── src/main/java/com/nucleusteq/session2/
 │              ├── controller/
 │              ├── service/
 │              ├── repository/
 │              ├── model/
 │              ├── component/
 │              └── exception/
 └── session1/
```

---
