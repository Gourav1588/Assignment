// ===============================
// INDEX PAGE SCRIPT (index.js)
// ===============================

// 1. Date Constraints Setup
// Handles minimum date selection logic for booking inputs
const startDateInput = document.getElementById('startDate');
const endDateInput = document.getElementById('endDate');

if (startDateInput && endDateInput) {

  // Set today's date as minimum selectable date
  const today = new Date().toISOString().split('T')[0];
  startDateInput.min = today;
  endDateInput.min = today;

  // Update return date minimum when pickup date changes
  startDateInput.addEventListener('change', function() {
    endDateInput.min = this.value;
  });
}

// 2. Button Actions

// Handle search button click
// Validates input and redirects to vehicles page
function handleSearch() {
  const start = document.getElementById('startDate').value;
  const end = document.getElementById('endDate').value;

  // Validate dates are selected
  if (!start || !end) {
    showToast('Please select your pickup and return dates');
    return;
  }

  // Validate return date is after pickup date
  if (new Date(end) <= new Date(start)) {
    showToast('Return date must be after pickup date');
    return;
  }

  // Show feedback and navigate to vehicles page
  showToast('Searching available vehicles...');
  setTimeout(() => {
    window.location.href = 'vehicles.html';
  }, 1000);
}

// Handle booking action
// Checks if user is authenticated before allowing booking
function handleBook(name) {

  // Retrieve authentication token from local storage
  const token = localStorage.getItem('token');

  // If user is not logged in, redirect to login page
  if (!token) {
    showToast('Please sign in to book ' + name);

    setTimeout(() => {
      window.location.href = 'login.html';
    }, 1500);

    return;
  }

  // If authenticated, proceed to vehicles page
  window.location.href = 'vehicles.html';
}

// Filter vehicles by category
// Shows feedback and redirects to filtered view
function filterCategory(cat) {
  showToast('Filtering by ' + cat + '...');

  setTimeout(() => {
    window.location.href = 'vehicles.html';
  }, 800);
}

});
