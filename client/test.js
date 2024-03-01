const data = {
    reviews: ["string123123"]
  };
  
fetch('http://localhost:8000/api/analyze/test', {
method: 'POST',
headers: {
    'Content-Type': 'application/json',
    'accept': 'application/json'
},
body: JSON.stringify(data),
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));

// const websocket = new WebSocket('ws://localhost:8000/api/analyze/ws/1');

// websocket.onopen = () => {
//   console.log('WebSocket connected');
// };

// websocket.onmessage = (event) => {
//   console.log('Message from server:', event.data);
// };

// websocket.onclose = () => {
//   console.log('WebSocket disconnected');
// };

// websocket.onerror = (error) => {
//   console.error('WebSocket error:', error);
// };
