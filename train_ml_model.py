import sqlite3
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix

# Load data from SQLite database
def load_data():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT latitude, longitude, altitude, is_authentic FROM gps_logs")
    data = cursor.fetchall()
    conn.close()
    
    X = np.array([row[:3] for row in data])  # Features (lat, lon, alt)
    y = np.array([row[3] for row in data])   # Labels (0 = Spoofed, 1 = Authentic)
    
    return X, y

# Load and preprocess data
X, y = load_data()
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train a Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)

print(f"✅ Model Training Complete!")
print(f"📊 Accuracy: {accuracy:.2f}")
print(f"🌀 Confusion Matrix:\n{conf_matrix}")

import joblib

# Save the trained model and scaler
joblib.dump(model, "gps_model.pkl")
joblib.dump(scaler, "scaler.pkl")

print("✅ Model and Scaler Saved Successfully!")
