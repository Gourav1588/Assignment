package com.nucleusteq.session2.controller;

import com.nucleusteq.session2.service.NotificationService;
import org.springframework.web.bind.annotation.*;

/**
 * Controller for Notification system.
 * Exposes a POST endpoint to trigger notifications.
 * The controller only receives the request and
 * passes it to the service, nothing more.
 */
@RestController
@RequestMapping("/notify")
public class NotificationController {

    // Constructor injection as required by the assignment
    private final NotificationService notificationService;

    /**
     * Spring injects NotificationService here automatically.
     */
    public NotificationController(NotificationService notificationService) {
        this.notificationService = notificationService;
    }

    /**
     * POST /notify
     * Triggers the notification flow and
     * returns a confirmation message to the client.
     */
    @PostMapping
    public String triggerNotification() {
        return notificationService.sendNotification();
    }
}