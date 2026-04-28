package com.vehicle.rental.security;

import com.vehicle.rental.entity.User;
import com.vehicle.rental.repository.UserRepository;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.web.authentication.WebAuthenticationDetailsSource;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.util.Optional;

/**
 * Core security interceptor that runs on every incoming HTTP request.
 * Extracts the JWT from the Authorization header, validates its signature and expiration,
 * and sets the authenticated user context for the duration of the request.
 */
@Slf4j
@Component
@RequiredArgsConstructor
public class JwtAuthenticationFilter extends OncePerRequestFilter {

    private final JwtService jwtService;
    private final UserRepository userRepository;

    @Override
    protected void doFilterInternal(
            HttpServletRequest request,
            HttpServletResponse response,
            FilterChain filterChain) throws ServletException, IOException {

        String authHeader = request.getHeader("Authorization");

        // Bypass filter if no Bearer token is present
        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            filterChain.doFilter(request, response);
            return;
        }

        String token = authHeader.substring(7);

        // Terminate authentication if token is forged or expired
        if (!jwtService.isTokenValid(token)) {
            log.error("Invalid or expired JWT token encountered.");
            filterChain.doFilter(request, response);
            return;
        }

        String email = jwtService.extractEmail(token);
        Optional<User> userOptional = userRepository.findByEmail(email);

        if (userOptional.isEmpty()) {
            filterChain.doFilter(request, response);
            return;
        }

        CustomUserDetails userDetails = new CustomUserDetails(userOptional.get());

        // Establish the security context for the current thread
        UsernamePasswordAuthenticationToken authToken =
                new UsernamePasswordAuthenticationToken(
                        userDetails,
                        null,
                        userDetails.getAuthorities()
                );

        authToken.setDetails(new WebAuthenticationDetailsSource().buildDetails(request));
        SecurityContextHolder.getContext().setAuthentication(authToken);

        log.debug("Successfully authenticated request for user: {}", email);

        filterChain.doFilter(request, response);
    }
}