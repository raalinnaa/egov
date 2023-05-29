const sendOtpForm = document.querySelector('#send-otp-form');

sendOtpForm.addEventListener('submit', event => {
	event.preventDefault();

	const orderId = sendOtpForm.elements.order_id.value;
	const token = localStorage.getItem('token');

	fetch(`http://127.0.0.1:8000/api/con/send_otp/?order_id=${orderId}`, {
		method: 'GET',
		headers: {
			'Authorization': `Token ${token}`,
			'Content-Type': 'application/json'
		}
	})
		.then(response => {
			if (!response.ok) {
				throw new Error('Unable to send OTP.');
			}
			return response.json();
		})
		.then(data => {
			alert('OTP sent successfully.');
			window.location.href = '../verify_otp';
		})
		.catch(error => {
			alert(error.message);
		});
});
