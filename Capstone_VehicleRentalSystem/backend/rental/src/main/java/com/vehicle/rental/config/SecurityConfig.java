package com.vehicle.rental.config;

import com.vehicle.rental.security.JwtAuthenticationFilter;
import lombok.RequiredArgsConstructor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

/**
 * Core security configuration for the application.
 * Manages CORS, CSRF, session policy, and endpoint authorization rules.
 */
@Configuration
@EnableWebSecurity
@EnableMethodSecurity
@RequiredArgsConstructor
public class SecurityConfig {

    private final JwtAuthenticationFilter jwtAuthFilter;

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {

        http
                // 1. Enable CORS using global configuration (CorsConfig.java)
                .cors(org.springframework.security.config.Customizer.withDefaults())

                // 2. Disable CSRF for stateless JWT APIs
                .csrf(csrf -> csrf.disable())

                // 3. Enforce stateless session management
                .sessionManagement(session -> session
                        .sessionCreationPolicy(SessionCreationPolicy.STATELESS))

                // 4. Define endpoint authorization rules
                .authorizeHttpRequests(auth -> auth
                        // CRITICAL: Allow browser CORS preflight checks (OPTIONS) to bypass authentication
                        .requestMatchers(HttpMethod.OPTIONS, "/**").permitAll()

                        // Public Endpoints
                        .requestMatchers("/api/auth/**").permitAll()
                        .requestMatchers(HttpMethod.GET, "/api/vehicles/**", "/api/categories/**").permitAll()

                        // All other endpoints require a valid JWT
                        .anyRequest().authenticated()
                )

                // 5. Register the custom JWT filter before standard authentication
                .addFilterBefore(
                        jwtAuthFilter,
                        UsernamePasswordAuthenticationFilter.class
                );

        return http.build();
    }

    /**
     * Provides the password hashing algorithm for the application.
     * @return BCryptPasswordEncoder instance.
     */
    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
}