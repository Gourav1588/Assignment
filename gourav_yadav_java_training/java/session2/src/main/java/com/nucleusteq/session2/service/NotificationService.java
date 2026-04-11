package com.nucleusteq.session2.service;

import com.nucleusteq.session2.component.NotificationComponent;
import org.springframework.stereotype.Service;

/**
 * Uses NotificationComponent to generate messages.
 */
@Service
public class NotificationService {

    // Component instance injected via constructor
    private final NotificationComponent notificationComponent;

    /**
     * Constructor injection of NotificationComponent.
     */
    public NotificationService(NotificationComponent notificationComponent) {
        this.notificationComponent = notificationComponent;
    }

    // Triggers notification and returns message
    public String sendNotification() {
        return notificationComponent.generateMessage();
    }
}