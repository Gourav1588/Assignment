package com.nucleusteq.session2.repository;

import com.nucleusteq.session2.model.User;
import org.springframework.stereotype.Repository;

import java.util.ArrayList;
import java.util.List;

/**
 * Repository layer for User.
 * Handles in-memory data storage and retrieval.
 */
@Repository
public class UserRepository {

    // In-memory list to store users (acts as our database)
    private final List<User> userList = new ArrayList<>();

    /**
     * Constructor to load dummy users at startup.
     */
    public UserRepository() {
        userList.add(new User(1, "Gourav", "gourav@gmail.com"));
        userList.add(new User(2, "Rahul", "rahul@gmail.com"));
        userList.add(new User(3, "Priya", "priya@gmail.com"));
    }

    // Returns all users from the list
    public List<User> findAll() {
        return userList;
    }

    /**
     * Searches for a user by their unique ID.
     * Returns the User if found, or null if no match exists.
     */
    public User findById(int id) {
        return userList.stream()
                .filter(user -> user.getId() == id )
                .findFirst()
                .orElse(null);
    }

    // Adds a new user to the list
    public User save(User user) {
        userList.add(user);
        return user;
    }
}