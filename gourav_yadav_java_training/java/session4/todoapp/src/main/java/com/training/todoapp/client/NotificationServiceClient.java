package com.training.todoapp.client;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

/*
 * I'm using this class to simulate an outbound call to an external notification provider.
 * I've kept it as a stub so the service layer can call it without any real dependency.
 */
@Service
public class NotificationServiceClient {

    // I'm initializing an SLF4J logger to track when our simulated events fire.
    private static final Logger log = LoggerFactory.getLogger(NotificationServiceClient.class);

    // I use specific event methods rather than a generic string to create a strict contract.
    public void onTodoCreated(Long id, String title) {
        log.info("Notification sent — todo created [id={}, title='{}']", id, title);
    }

    public void onTodoStatusChanged(Long id, String from, String to) {
        log.info("Notification sent — status changed [id={}, {} -> {}]", id, from, to);
    }

    public void onTodoDeleted(Long id) {
        log.info("Notification sent — todo deleted [id={}]", id);
    }
}