package com.nucleusteq.session3.model;

/*
 * This class represents a User entity in our application.
 * We use this class to store and transfer user-related data
 * between different layers like controller, service, and repository.
 */
public class User {
    private int id;
    private String name;

    // Stores the age of the user
    private int age;
    private String role;

    /*
     * Instead of setting values one by one, we initialize everything at once.
     */
    public User(int id, String name, int age, String role) {
        this.id = id;
        this.name = name;
        this.age = age;
        this.role = role;
    }

    // Getter methods are used to read/access the values of variables

    public int getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public int getAge() {
        return age;
    }

    public String getRole() {
        return role;
    }

    // Setter methods are used to update/change the values when needed

    public void setId(int id) {
        this.id = id;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void setAge(int age) {
        this.age = age;
    }

    public void setRole(String role) {
        this.role = role;
    }
}