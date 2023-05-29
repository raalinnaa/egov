const form = document.querySelector('#login-form');

form.addEventListener('submit', async (event) => {
	event.preventDefault();

	const email = event.target.email.value;
	const password = event.target.password.value;

	try {
		const response = await fetch('http://localhost:8000/api/users/login/', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ email, password })
		});

		if (!response.ok) {
			const data = await response.json();
			throw new Error(data.message);
		}

		const data = await response.json();
		localStorage.setItem('token', data.token);
		// alert('Login successful!');
    // Redirect to home page
    window.location.href = '../main';
	} catch (error) {
		alert("There is an error!");
	}
});
