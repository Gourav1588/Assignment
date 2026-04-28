# Vehicle Rental System – Database Design (ERD)

---

## Overview

This system uses PostgreSQL and is built on four core entities:

* users
* vehicle_categories
* vehicles
* bookings

These support:

* authentication
* vehicle management
* booking operations

---

## Entities

---

### 1. Users

Stores all registered users (USER and ADMIN).

| Key | Column     | Type         | Constraints            | Description              |
| --- | ---------- | ------------ | ---------------------- | ------------------------ |
| PK  | id         | BIGINT       | PRIMARY KEY, IDENTITY  | Auto-generated user ID   |
|     | name       | VARCHAR(255) | NOT NULL               | Full name                |
|     | email      | VARCHAR(255) | NOT NULL, UNIQUE       | Unique login email       |
|     | password   | VARCHAR(255) | NOT NULL               | Hashed password (BCrypt) |
|     | role       | VARCHAR(50)  | NOT NULL, DEFAULT USER | USER or ADMIN            |
|     | created_at | TIMESTAMP    | NOT NULL               | Created timestamp        |

---

### 2. Vehicle Categories

Stores categories dynamically.

Examples:

* Sedan
* SUV
* Bike

| Key | Column      | Type         | Constraints           | Description   |
| --- | ----------- | ------------ | --------------------- | ------------- |
| PK  | id          | BIGINT       | PRIMARY KEY, IDENTITY | Category ID   |
|     | name        | VARCHAR(255) | NOT NULL, UNIQUE      | Category name |
|     | description | TEXT         | NULLABLE              | Description   |

---

### 3. Vehicles

Stores all vehicles.

| Key | Column        | Type         | Constraints           | Description        |
| --- | ------------- | ------------ | --------------------- | ------------------ |
| PK  | id            | BIGINT       | PRIMARY KEY, IDENTITY | Vehicle ID         |
| FK  | category_id   | BIGINT       | NULLABLE              | Category reference |
|     | name          | VARCHAR(255) | NOT NULL              | Vehicle name       |
|     | type          | VARCHAR(50)  | NOT NULL              | CAR or BIKE        |
|     | is_active     | BOOLEAN      | DEFAULT true          | Soft delete flag   |
|     | description   | TEXT         | NULLABLE              | Details            |
|     | price_per_day | DOUBLE       | NOT NULL              | Price per day      |
|     | created_at    | TIMESTAMP    | NOT NULL              | Created time       |

---

### 4. Bookings

Stores all bookings.

| Key | Column     | Type        | Constraints           | Description       |
| --- | ---------- | ----------- | --------------------- | ----------------- |
| PK  | id         | BIGINT      | PRIMARY KEY, IDENTITY | Booking ID        |
| FK  | user_id    | BIGINT      | NOT NULL              | User reference    |
| FK  | vehicle_id | BIGINT      | NOT NULL              | Vehicle reference |
|     | start_date | DATE        | NOT NULL              | Start date        |
|     | end_date   | DATE        | NOT NULL              | End date          |
|     | total_cost | DOUBLE      | NOT NULL              | Total price       |
|     | status     | VARCHAR(50) | DEFAULT PENDING       | Booking status    |
|     | created_at | TIMESTAMP   | NOT NULL              | Created time      |

---

## Relationships

### Users → Bookings

One user can create multiple bookings

```
USERS ──o{ BOOKINGS
```

---

### Vehicle Categories → Vehicles

One category can contain multiple vehicles

```
VEHICLE_CATEGORIES ──o{ VEHICLES
```

---

### Vehicles → Bookings

One vehicle can be booked multiple times

```
VEHICLES ──o{ BOOKINGS
```

---

## Key Design Decisions

* Passwords are stored securely using BCrypt hashing
* Roles stored as strings (USER, ADMIN)
* Soft delete implemented using `is_active`
* Booking cost stored as snapshot
* Double booking prevented using date validation

---

## System Flow (High-Level)

```
Client Request
      ↓
Controller
      ↓
Service Layer
      ↓
Repository (JPA)
      ↓
Database
      ↓
Response returned
```

---

## Authentication Flow (JWT)

```
Login/Register
      ↓
AuthService
      ↓
JWT Token Generated
      ↓
Client stores token
      ↓
Request with token
      ↓
JwtAuthenticationFilter
      ↓
SecurityContext updated
      ↓
Controller access granted
```

---

## Summary

This design ensures:

* Secure authentication system
* Scalable vehicle management
* Reliable booking mechanism
* Clean separation of concerns
* Strong relational integrity

---
