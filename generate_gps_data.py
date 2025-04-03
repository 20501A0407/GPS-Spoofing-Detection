import random
import sqlite3
from datetime import datetime

# Function to log GPS data into SQLite database
def log_event_db(gps_signal, is_authentic):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gps_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp INTEGER,
            latitude REAL,
            longitude REAL,
            altitude REAL,
            is_authentic INTEGER
        )
    ''')
    
    cursor.execute("INSERT INTO gps_logs (timestamp, latitude, longitude, altitude, is_authentic) VALUES (?, ?, ?, ?, ?)",
                   (gps_signal["timestamp"], gps_signal["latitude"], gps_signal["longitude"], gps_signal["altitude"], int(is_authentic)))
    
    conn.commit()
    conn.close()

# Function to generate random GPS signals
def generate_random_gps_data(is_spoofed=False):
    base_lat, base_lon, base_alt = 37.7749, -122.4194, 30.0  # Base location (San Francisco)
    lat_jitter, lon_jitter, alt_jitter = random.uniform(-0.01, 0.01), random.uniform(-0.01, 0.01), random.uniform(-5, 5)

    if is_spoofed:
        lat_jitter, lon_jitter, alt_jitter = random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-50, 50)

    return {
        "timestamp": int(datetime.utcnow().timestamp()),
        "latitude": base_lat + lat_jitter,
        "longitude": base_lon + lon_jitter,
        "altitude": base_alt + alt_jitter,
    }

# Generate and Log GPS Data
for _ in range(100):  # Increased from 10 to 100 samples
    log_event_db(generate_random_gps_data(is_spoofed=False), True)
    log_event_db(generate_random_gps_data(is_spoofed=True), False)

print("✅ GPS Data Logged Successfully! Run `train_ml_model.py` to train the model.")