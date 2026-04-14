package com.nucleusteq.session3.repository;

import com.nucleusteq.session3.model.User;
import org.springframework.stereotype.Repository;

import java.util.ArrayList;
import java.util.List;

/**
 * Repository layer responsible for data management.
 * Marked with @Repository to allow Spring's IoC container to manage it as a bean.
 */
@Repository
public class UserRepository {

    /**
     * Using an in-memory ArrayList to store user data.
     */
    private final List<User> users = new ArrayList<>();

    /**
     * Constructor used to initialize the system with dummy data.
     */
    public UserRepository() {

        users.add(new User(1, "Priya", 25, "ADMIN"));
        users.add(new User(2, "Rahul", 30, "USER"));
        users.add(new User(3, "Anjali", 28, "USER"));
        users.add(new User(4, "Gourav", 30, "ADMIN"));
        users.add(new User(5, "Sneha", 22, "USER"));
        users.add(new User(6, "Arjun", 35, "MANAGER"));
        users.add(new User(7, "Meera", 28, "USER"));
    }

    /**
     * Fetches the entire list of users from the in-memory storage.
     * This is used by the Service layer to begin the filtering process.
     */
    public List<User> findAll() {
        return users;
    }
}