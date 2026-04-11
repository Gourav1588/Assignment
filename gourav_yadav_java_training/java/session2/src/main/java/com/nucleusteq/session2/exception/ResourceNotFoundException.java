package com.nucleusteq.session2.exception;

// Custom exception for cases when something is not found (like user)
public class ResourceNotFoundException extends RuntimeException {

    // pass message to RuntimeException so we can return it in response
    public ResourceNotFoundException(String message) {
        super(message);
    }
}