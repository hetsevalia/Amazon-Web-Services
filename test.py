import mysql.connector
import pickle
import numpy as np

# Load the trained model
with open("diabetes_model.pkl", "rb") as file:
    model = pickle.load(file)

# MySQL connection function
def connect_db():
    return mysql.connector.connect(
        host="diabetes-prediction-database.cp8meyc8q5hq.ap-south-1.rds.amazonaws.com",  # Change this if you're using a remote MySQL server (e.g., AWS RDS)
        user="admin",       # Your MySQL username
        password="adminDiabetes2830",  # Your MySQL password
        database="DiabetesPredictionDB"  # Your MySQL database name
    )

# Function to insert data into MySQL and make predictions
def insert_and_predict(data):
    # Convert input to numpy array for prediction
    data_array = np.array([[ 
        data['Pregnancies'], data['Glucose'], data['BloodPressure'],
        data['SkinThickness'], data['Insulin'], data['BMI'],
        data['DiabetesPedigreeFunction'], data['Age']
    ]])

    # Make prediction using the model
    prediction = model.predict(data_array)
    result = "Diabetic" if prediction[0] == 1 else "Non-diabetic"

    # Convert numpy data types to native Python types before inserting
    data = {key: (value.item() if isinstance(value, np.generic) else value) for key, value in data.items()}
    
    # Connect to the database
    conn = connect_db()
    cursor = conn.cursor()

    # Insert data into the PatientData table
    cursor.execute("""
        INSERT INTO PatientData (Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age, diabetic)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data['Pregnancies'], data['Glucose'], data['BloodPressure'], data['SkinThickness'],
        data['Insulin'], data['BMI'], data['DiabetesPedigreeFunction'], data['Age'], int(prediction[0])
    ))

    # Commit and close the connection
    conn.commit()
    cursor.close()
    conn.close()

    return result

# Example input data for testing
input_data = {
    'Pregnancies': 3,
    'Glucose': 120,
    'BloodPressure': 70,
    'SkinThickness': 20,
    'Insulin': 80,
    'BMI': 25.6,
    'DiabetesPedigreeFunction': 0.5,
    'Age': 32
}

# Insert the data and get the prediction
prediction_result = insert_and_predict(input_data)

print(f"Prediction Result: {prediction_result}")