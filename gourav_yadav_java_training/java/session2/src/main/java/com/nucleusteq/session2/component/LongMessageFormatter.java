package com.nucleusteq.session2.component;

import org.springframework.stereotype.Component;

// This tells Spring to automatically detect and create an object of this class
// No need to manually instantiate it anywhere
@Component
public class LongMessageFormatter implements MessageFormatter {


    @Override
    public String format() {
        return "Hello! This is a detailed long message. It provides more depth and explanation.";
    }

    // This method identifies this formatter's type
    // It is used as a key while building the Map in MessageService
    // When user passes type=LONG → this formatter gets selected
    @Override
    public String getType() {
        return "LONG";
    }
}