package com.nucleusteq.session2.controller;

import com.nucleusteq.session2.service.MessageService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

// This annotation tells Spring that this class will handle REST API requests
@RestController

// Base URL mapping for this controller → all endpoints will start with /message
@RequestMapping("/message")
public class MessageController {

    // We are not creating MessageService manually
    // Spring will inject it for us (Dependency Injection)
    private final MessageService messageService;


    public MessageController(MessageService messageService) {
        this.messageService = messageService;
    }

    // This method handles GET requests like:
    // http://localhost:8080/message?type=short
    @GetMapping
    public String getMessage(@RequestParam String type) {

        // @RequestParam is used to take input from URL query parameter
        // Example: ?type=morning → "morning" will be passed to this method

        return messageService.getMessage(type);
    }
}