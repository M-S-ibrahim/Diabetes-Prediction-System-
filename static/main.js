document.addEventListener('DOMContentLoaded', function() {
    console.log("JavaScript is loaded and running!");

    const form = document.getElementById('prediction-form');
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission

        const formData = new FormData(form); // Collect form data
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });

        fetch('/predict', { // Send data to the prediction endpoint
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('result').innerText = `Prediction: ${data.prediction}`;
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });
});
