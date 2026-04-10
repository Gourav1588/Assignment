package com.nucleusteq.session2.component;

public interface MessageFormatter {
    String format();
    String getType(); // Used by the service to identify the format type
}