const token = localStorage.getItem('token');

if (!token) {
	window.location.href = '/login.html';
}

const ordersList = document.querySelector('#orders-list');

fetch('http://127.0.0.1:8000/api/con/2/orders/', {
	method: 'GET',
	headers: {
		'Authorization': `Token ${token}`,
		'Content-Type': 'application/json'
	}
})
	.then(response => {
		if (!response.ok) {
			throw new Error('Unable to fetch orders.');
		}
		return response.json();
	})
	.then(data => {
		data.forEach(order => {
			const orderElement = document.createElement('li');
			orderElement.classList.add('order');

			const orderId = document.createElement('div');
			orderId.textContent = `Order ID: ${order.id}`;

			const orderStatus = document.createElement('div');
			orderStatus.classList.add('order-status');
			orderStatus.textContent = order.status;

			const orderDetails = document.createElement('div');
			orderDetails.textContent = `Client IIN: ${order.client_iin}, Taker IIN: ${order.taker_iin}`;

			orderElement.appendChild(orderId);
			orderElement.appendChild(orderStatus);
			orderElement.appendChild(orderDetails);

			ordersList.appendChild(orderElement);
		});
	})
	.catch(error => {
		alert(error.message);
	});
