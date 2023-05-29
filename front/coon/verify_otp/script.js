// Get elements from HTML
const form = document.querySelector('form');
const otpCode = document.querySelector('#otp-code');
const submitBtn = document.querySelector('#submit-btn');
const errorBox = document.querySelector('#error-box');

// Get order ID and OTP code from URL query params
const urlParams = new URLSearchParams(window.location.search);
const orderId = urlParams.get('order_id');
const otp = urlParams.get('otp_code');

// Set order ID in HTML
document.querySelector('#order-id').textContent = orderId;

// Add event listener to form submission
form.addEventListener('submit', (event) => {
  event.preventDefault(); // Prevent form submission

  // Send request to verify OTP code
  const url = `http://127.0.0.1:8000/api/con/verify_otp/?order_id=${orderId}&otp_code=${otpCode.value}`;
  const token = localStorage.getItem('token');
  fetch(url, {
    headers: {
      'Authorization': `Token ${token}`
    }
  })
  .then(response => {
    if (response.ok) {
      // OTP code is correct, show success message
      errorBox.classList.remove('show');
      const successBox = document.querySelector('#success-box');
      successBox.classList.add('show');
    } else {
      // OTP code is incorrect, show error message
      errorBox.classList.add('show');
    }
  })
  .catch(error => {
    // Show error message if there is a network error
    errorBox.classList.add('show');
  })
});
