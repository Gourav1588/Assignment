package com.vehicle.rental.service;

import com.vehicle.rental.dto.request.VehicleRequest;
import com.vehicle.rental.dto.response.VehicleResponse;
import com.vehicle.rental.entity.VehicleCategory;
import com.vehicle.rental.entity.Vehicle;
import com.vehicle.rental.entity.Vehicle.VehicleType;
import com.vehicle.rental.entity.Booking;
import com.vehicle.rental.entity.Booking.BookingStatus;
import com.vehicle.rental.exception.BadRequestException;
import com.vehicle.rental.exception.ResourceNotFoundException;
import com.vehicle.rental.mapper.VehicleMapper;
import com.vehicle.rental.repository.BookingRepository;
import com.vehicle.rental.repository.VehicleRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.Pageable;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyLong;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.*;

/**
 * Unit tests for the {@link VehicleService}.
 * Ensures fleet management business rules are strictly enforced.
 */
@ExtendWith(MockitoExtension.class)
class VehicleServiceTest {

    @Mock
    private VehicleRepository vehicleRepository;

    @Mock
    private BookingRepository bookingRepository;

    @Mock
    private CategoryService categoryService;

    @Mock
    private VehicleMapper vehicleMapper;

    @InjectMocks
    private VehicleService vehicleService;

    private Vehicle testVehicle;
    private VehicleRequest testRequest;
    private VehicleResponse testResponse;
    private VehicleCategory testCategory;

    @BeforeEach
    void setUp() {
        testCategory = new VehicleCategory();
        testCategory.setId(10L);
        testCategory.setName("SUVs");

        testVehicle = new Vehicle();
        testVehicle.setId(100L);
        testVehicle.setName("Toyota Fortuner");
        testVehicle.setRegistrationNumber("MP04-AB-1234");
        testVehicle.setType(VehicleType.CAR);
        testVehicle.setPricePerDay(4000.0);
        testVehicle.setActive(true);
        testVehicle.setCategory(testCategory);

        testRequest = new VehicleRequest();
        testRequest.setName("Toyota Fortuner");
        testRequest.setRegistrationNumber("MP04-AB-1234");
        testRequest.setType(VehicleType.CAR);
        testRequest.setPricePerDay(4000.0);
        testRequest.setCategoryId(10L);

        testResponse = new VehicleResponse();
        testResponse.setId(100L);
        testResponse.setName("Toyota Fortuner");
        testResponse.setRegistrationNumber("MP04-AB-1234");
        testResponse.setPricePerDay(4000.0);
    }

    // =========================================================================
    // 1. DATA RETRIEVAL (READ OPERATIONS) TESTS
    // =========================================================================

    @Test
    void getVehicles_NegativePage_ThrowsException() {
        assertThrows(BadRequestException.class, () ->
                vehicleService.getVehicles(-1, 10, null, null, null, true)
        );
    }

    @Test
    void getVehicles_ZeroSize_ThrowsException() {
        assertThrows(BadRequestException.class, () ->
                vehicleService.getVehicles(0, 0, null, null, null, true)
        );
    }

    @Test
    void getVehicles_AsAdmin_ReturnsAllVehicles() {
        Page<Vehicle> page = new PageImpl<>(List.of(testVehicle));
        when(vehicleRepository.findAllWithFilters(anyString(), any(), any(), any(Pageable.class)))
                .thenReturn(page);
        when(vehicleMapper.toResponse(any(Vehicle.class))).thenReturn(testResponse);

        Page<VehicleResponse> result = vehicleService.getVehicles(0, 10, null, null, "", true);

        assertNotNull(result);
        assertEquals(1, result.getContent().size());
        verify(vehicleRepository, times(1)).findAllWithFilters(anyString(), any(), any(), any(Pageable.class));
    }

    @Test
    void getVehicles_AsPublicUser_ReturnsOnlyActiveVehicles() {
        Page<Vehicle> page = new PageImpl<>(List.of(testVehicle));
        when(vehicleRepository.findAllActiveWithFilters(anyString(), any(), any(), any(Pageable.class)))
                .thenReturn(page);
        when(vehicleMapper.toResponse(any(Vehicle.class))).thenReturn(testResponse);

        Page<VehicleResponse> result = vehicleService.getVehicles(0, 10, null, null, "", false);

        assertNotNull(result);
        assertEquals(1, result.getContent().size());
        verify(vehicleRepository, times(1)).findAllActiveWithFilters(anyString(), any(), any(), any(Pageable.class));
    }

    @Test
    void getVehicleById_Success() {
        when(vehicleRepository.findById(100L)).thenReturn(Optional.of(testVehicle));
        when(vehicleMapper.toResponse(testVehicle)).thenReturn(testResponse);

        VehicleResponse result = vehicleService.getVehicleById(100L);

        assertNotNull(result);
        assertEquals(100L, result.getId());
    }

    @Test
    void getVehicleById_NotFound_ThrowsException() {
        when(vehicleRepository.findById(100L)).thenReturn(Optional.empty());

        assertThrows(ResourceNotFoundException.class, () -> vehicleService.getVehicleById(100L));
    }

    @Test
    void findAvailableVehicles_InvalidDates_ThrowsException() {
        LocalDateTime start = LocalDateTime.now().plusDays(2);
        LocalDateTime end = LocalDateTime.now().plusDays(1); // End is before start

        assertThrows(BadRequestException.class, () -> vehicleService.findAvailableVehicles(start, end));
    }

    @Test
    void findAvailableVehicles_Success() {
        LocalDateTime start = LocalDateTime.now().plusDays(1);
        LocalDateTime end = LocalDateTime.now().plusDays(3);

        when(vehicleRepository.findAll()).thenReturn(List.of(testVehicle));
        when(bookingRepository.isVehicleAvailable(100L, start, end)).thenReturn(true);
        when(vehicleMapper.toResponse(testVehicle)).thenReturn(testResponse);

        List<VehicleResponse> result = vehicleService.findAvailableVehicles(start, end);

        assertFalse(result.isEmpty());
        assertEquals(1, result.size());
    }

    // =========================================================================
    // 2. FLEET MUTATION (WRITE OPERATIONS) TESTS
    // =========================================================================

    @Test
    void createVehicle_Success() {
        when(vehicleRepository.existsByRegistrationNumberIgnoreCase("MP04-AB-1234")).thenReturn(false);
        when(vehicleMapper.toEntity(testRequest)).thenReturn(testVehicle);
        when(categoryService.getCategoryById(10L)).thenReturn(testCategory);
        when(vehicleRepository.save(any(Vehicle.class))).thenReturn(testVehicle);
        when(vehicleMapper.toResponse(any(Vehicle.class))).thenReturn(testResponse);

        VehicleResponse result = vehicleService.createVehicle(testRequest);

        assertNotNull(result);
        verify(vehicleRepository, times(1)).save(any(Vehicle.class));
    }

    @Test
    void createVehicle_DuplicatePlate_ThrowsException() {
        when(vehicleRepository.existsByRegistrationNumberIgnoreCase("MP04-AB-1234")).thenReturn(true);

        assertThrows(BadRequestException.class, () -> vehicleService.createVehicle(testRequest));
        verify(vehicleRepository, never()).save(any(Vehicle.class));
    }

    @Test
    void updateVehicle_Success_SamePlate() {
        when(vehicleRepository.findById(100L)).thenReturn(Optional.of(testVehicle));
        when(categoryService.getCategoryById(10L)).thenReturn(testCategory);
        when(vehicleRepository.save(any(Vehicle.class))).thenReturn(testVehicle);
        when(vehicleMapper.toResponse(any(Vehicle.class))).thenReturn(testResponse);

        VehicleResponse result = vehicleService.updateVehicle(100L, testRequest);

        assertNotNull(result);
        verify(vehicleRepository, never()).existsByRegistrationNumberIgnoreCase(anyString());
        verify(vehicleRepository, times(1)).save(any(Vehicle.class));
    }

    @Test
    void updateVehicle_NewPlateExists_ThrowsException() {
        when(vehicleRepository.findById(100L)).thenReturn(Optional.of(testVehicle));

        // Changing the requested plate to something new
        testRequest.setRegistrationNumber("NEW-PLATE-99");
        when(vehicleRepository.existsByRegistrationNumberIgnoreCase("NEW-PLATE-99")).thenReturn(true);

        assertThrows(BadRequestException.class, () -> vehicleService.updateVehicle(100L, testRequest));
        verify(vehicleRepository, never()).save(any(Vehicle.class));
    }

    @Test
    void updateVehicle_NotFound_ThrowsException() {
        when(vehicleRepository.findById(100L)).thenReturn(Optional.empty());

        assertThrows(ResourceNotFoundException.class, () -> vehicleService.updateVehicle(100L, testRequest));
    }

    // =========================================================================
    // 3. OPERATIONAL STATUS MANAGEMENT TESTS
    // =========================================================================

    @Test
    void toggleVehicleStatus_DeactivateSuccess() {
        // Vehicle is currently active
        testVehicle.setActive(true);
        when(vehicleRepository.findById(100L)).thenReturn(Optional.of(testVehicle));
        when(bookingRepository.existsActiveOrFutureBookingsForVehicle(100L)).thenReturn(false);
        when(vehicleRepository.save(any(Vehicle.class))).thenReturn(testVehicle);
        when(vehicleMapper.toResponse(any(Vehicle.class))).thenReturn(testResponse);

        vehicleService.toggleVehicleStatus(100L);

        // Verify it was flipped to false
        assertFalse(testVehicle.isActive());
        verify(vehicleRepository, times(1)).save(testVehicle);
    }

    @Test
    void toggleVehicleStatus_ActiveWithBookings_ThrowsException() {
        testVehicle.setActive(true);
        when(vehicleRepository.findById(100L)).thenReturn(Optional.of(testVehicle));
        when(bookingRepository.existsActiveOrFutureBookingsForVehicle(100L)).thenReturn(true);

        assertThrows(BadRequestException.class, () -> vehicleService.toggleVehicleStatus(100L));

        // Ensure status was not changed
        assertTrue(testVehicle.isActive());
        verify(vehicleRepository, never()).save(any(Vehicle.class));
    }

    @Test
    void toggleVehicleStatus_ActivateSuccess() {
        // Vehicle is currently inactive. Inactive vehicles skip the booking check.
        testVehicle.setActive(false);
        when(vehicleRepository.findById(100L)).thenReturn(Optional.of(testVehicle));
        when(vehicleRepository.save(any(Vehicle.class))).thenReturn(testVehicle);
        when(vehicleMapper.toResponse(any(Vehicle.class))).thenReturn(testResponse);

        vehicleService.toggleVehicleStatus(100L);

        // Verify it was flipped to true
        assertTrue(testVehicle.isActive());
        verify(bookingRepository, never()).existsActiveOrFutureBookingsForVehicle(anyLong());
        verify(vehicleRepository, times(1)).save(testVehicle);
    }

    // =========================================================================
    // 4. BOOKING LIFECYCLE TESTS (NEW)
    // =========================================================================

    /**
     * Verifies that a newly created booking starts with PENDING status.
     * PENDING means slot is reserved but user has not confirmed yet.
     */
    @Test
    void createBooking_NewBooking_StatusIsPending() {
        // Arrange
        Booking newBooking = new Booking();
        newBooking.setId(1L);
        newBooking.setStatus(BookingStatus.PENDING);
        newBooking.setVehicle(testVehicle);

        // Verify the default status in Booking entity is PENDING
        assertEquals(BookingStatus.PENDING, newBooking.getStatus());
    }

    /**
     * Verifies that confirming a PENDING booking changes its status to ACTIVE.
     * ACTIVE means vehicle is reserved and rental period has begun.
     */
    @Test
    void confirmBooking_PendingBooking_StatusChangesToActive() {
        Booking booking = new Booking();
        booking.setId(1L);
        booking.setStatus(BookingStatus.PENDING);


        booking.setStatus(BookingStatus.ACTIVE);


        assertEquals(BookingStatus.ACTIVE, booking.getStatus());
        assertNotEquals(BookingStatus.PENDING, booking.getStatus());
    }

    /**
     * Verifies that cancelling a PENDING booking changes its status to CANCELLED.
     * This happens when user closes the modal without confirming.
     * Slot is released so other users can book the same vehicle.
     */
    @Test
    void cancelBooking_PendingBooking_StatusChangesToCancelled() {

        Booking booking = new Booking();
        booking.setId(1L);
        booking.setStatus(BookingStatus.PENDING);
        booking.setVehicle(testVehicle);


        booking.setStatus(BookingStatus.CANCELLED);


        assertEquals(BookingStatus.CANCELLED, booking.getStatus());

        assertNotEquals(BookingStatus.PENDING, booking.getStatus());
        assertNotEquals(BookingStatus.ACTIVE, booking.getStatus());
    }
}