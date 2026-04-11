package com.nucleusteq.session2.service;

import com.nucleusteq.session2.model.User;
import com.nucleusteq.session2.repository.UserRepository;
import org.springframework.stereotype.Service;
import com.nucleusteq.session2.exception.ResourceNotFoundException;

import java.util.List;

/**

 * Contains all business logic for user operations.
 */
@Service
public class UserService {

    // Repository instance injected via constructor
    private final UserRepository userRepository;

    /**
     * Constructor injection of UserRepository.
     */
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    // Fetches all users from repository
    public List<User> getAllUsers() {
        return userRepository.findAll();
    }

    // Fetches a single user by id from repository
    // Throw when user not found
    public User getUserById(int id) {
        User user = userRepository.findById(id);
        if (user == null) {
            throw new ResourceNotFoundException(
                    "User not found with id: " + id);
        }
        return user;
    }

    // Assigns new id to user and saves via repository
    public User createUser(User user) {
        return userRepository.save(user);
    }
}