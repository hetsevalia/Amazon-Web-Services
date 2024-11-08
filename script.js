function makePrediction() {
    const button = document.querySelector("button");
    button.disabled = true;
    button.textContent = "Predicting...";

    // Collect input data from the form
    const data = {
        Pregnancies: parseInt(document.getElementById("pregnancies").value),
        Glucose: parseFloat(document.getElementById("glucose").value),
        BloodPressure: parseFloat(document.getElementById("bloodPressure").value),
        SkinThickness: parseFloat(document.getElementById("skinThickness").value),
        Insulin: parseFloat(document.getElementById("insulin").value),
        BMI: parseFloat(document.getElementById("bmi").value),
        DiabetesPedigreeFunction: parseFloat(document.getElementById("diabetesPedigree").value),
        Age: parseInt(document.getElementById("age").value)
    };

    // Validate inputs before sending
    if (Object.values(data).includes(NaN) || Object.values(data).includes(null)) {
        document.getElementById("result").textContent = "Error: Please fill all the fields correctly.";
        button.disabled = false;
        button.textContent = "Predict";
        return;
    }

    // Send the data to the FastAPI backend for prediction
    fetch("https://mg2jcqaijq7fb2r5qbno5wtvya0eccqr.lambda-url.ap-south-1.on.aws/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        // Display the prediction result
        if (data.prediction) {
            document.getElementById("result").textContent = `Prediction: ${data.prediction}`;
        } else {
            document.getElementById("result").textContent = "Error: No prediction received.";
        }
        button.disabled = false;
        button.textContent = "Predict";
    })
    .catch(error => {
        // Handle errors from the fetch request
        document.getElementById("result").textContent = "Error: Could not get prediction. Please try again.";
        console.error("Error during prediction:", error);  // Log the error to the console for debugging
        button.disabled = false;
        button.textContent = "Predict";
    });
}
