package com.nucleusteq.session2.component;

import org.springframework.stereotype.Component;

/**
 *  This Component responsible for generating notification messages.
 * Acts as a helper class for NotificationService.
 */
@Component
public class NotificationComponent {

    // Generates and returns a notification message
    public String generateMessage() {
        return "Notification sent successfully!";
    }
}