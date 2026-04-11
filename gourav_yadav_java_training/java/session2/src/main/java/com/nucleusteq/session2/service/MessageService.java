package com.nucleusteq.session2.service;

import com.nucleusteq.session2.component.MessageFormatter;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;


// Spring will automatically detect and manage this class as a bean
@Service
public class MessageService {

    // Map is used for fast lookup instead of looping every time
    // Key → type (SHORT, LONG)
    // Value → corresponding formatter implementation
    private final Map<String, MessageFormatter> formatters;

    // Constructor Injection:
    // Spring automatically injects ALL beans that implement MessageFormatter
    // as a List → no need to manually create objects
    public MessageService(List<MessageFormatter> formatterList) {

        // Converting List → Map for better performance
        // Instead of iterating list every time, we directly access by key (O(1))
        this.formatters = formatterList.stream()
                .collect(Collectors.toMap(
                        f -> f.getType().toUpperCase(),
                        f -> f
                ));
    }

    public String getMessage(String type) {

        // Convert input to uppercase to avoid case mismatch issues

        MessageFormatter formatter = formatters.get(type.toUpperCase());


        // Throw when invalid type passed
        if (formatter == null) {
            throw new IllegalArgumentException(
                    "Invalid type: " + type + ". Please use SHORT or LONG.");
        }

        return formatter.format();
    }
}