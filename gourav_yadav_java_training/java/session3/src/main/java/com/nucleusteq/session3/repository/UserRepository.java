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

        users.add(new User(1, "Mayur", 25, "ADMIN"));
        users.add(new User(2, "Niraj", 30, "USER"));
        users.add(new User(3, "Ajay", 28, "USER"));
        users.add(new User(4, "Gourav", 30, "ADMIN"));
        users.add(new User(5, "vikas", 22, "USER"));
        users.add(new User(6, "Ankit", 35, "MANAGER"));
        users.add(new User(7, "Monu", 28, "USER"));
    }

    /**
     * Fetches the entire list of users from the in-memory storage.
     * This is used by the Service layer to begin the filtering process.
     */
    public List<User> findAll() {
        return users;
    }

    public boolean deleteUserById(int id) {
        // This  removes the user from the 'users' list
        return users.removeIf(user -> user.getId() == id);
    }

    public void save(User user) {
        users.add(user);
    }
}