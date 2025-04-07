import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import joblib
import numpy as np
import folium
from geopy.geocoders import Nominatim
from folium.plugins import MarkerCluster
import webbrowser

def detect_spoofing(latitude, longitude, altitude):
    input_data = np.array([[latitude, longitude, altitude]])
    input_data = scaler.transform(input_data)
    prediction = model.predict(input_data)
    return "✅ Authentic" if prediction[0] == 1 else "⚠️ Spoofed"

def save_to_db(latitude, longitude, altitude, detection_result):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gps_signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            latitude REAL,
            longitude REAL,
            altitude REAL,
            detection_result TEXT
        )
    """)
    cursor.execute("INSERT INTO gps_signals (latitude, longitude, altitude, detection_result) VALUES (?, ?, ?, ?)",
                   (latitude, longitude, altitude, detection_result))
    conn.commit()
    conn.close()

def generate_map():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT latitude, longitude, detection_result FROM gps_signals")
    data = cursor.fetchall()
    conn.close()
    
    if not data:
        messagebox.showwarning("No Data", "No GPS signals found in the database.")
        return
    
    map_center = [data[0][0], data[0][1]]
    gps_map = folium.Map(location=map_center, zoom_start=5)
    marker_cluster = MarkerCluster().add_to(gps_map)
    
    for lat, lon, result in data:
        color = "green" if "Authentic" in result else "red"
        folium.Marker([lat, lon], popup=f"{result}", icon=folium.Icon(color=color)).add_to(marker_cluster)
    
    gps_map.save("gps_map.html")
    webbrowser.open("gps_map.html")

def process_input():
    try:
        latitude = float(lat_entry.get())
        longitude = float(lon_entry.get())
        altitude = float(alt_entry.get())
        detection_result = detect_spoofing(latitude, longitude, altitude)
        save_to_db(latitude, longitude, altitude, detection_result)
        result_label.config(text=f"Detection Result: {detection_result}", foreground="green" if "Authentic" in detection_result else "red")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numeric values for Latitude, Longitude, and Altitude.")

# GUI Setup
root = tk.Tk()
root.title("GPS Spoofing Detection")
root.geometry("420x400")
root.configure(bg="#F0F0F0")

frame = ttk.Frame(root, padding=20)
frame.pack(expand=True)

label = ttk.Label(frame, text="Enter GPS Coordinates", font=("Arial", 14, "bold"))
label.grid(row=0, column=0, columnspan=2, pady=10)

lat_label = ttk.Label(frame, text="Latitude:")
lat_label.grid(row=1, column=0, sticky="w", pady=5)
lat_entry = ttk.Entry(frame)
lat_entry.grid(row=1, column=1, pady=5)

lon_label = ttk.Label(frame, text="Longitude:")
lon_label.grid(row=2, column=0, sticky="w", pady=5)
lon_entry = ttk.Entry(frame)
lon_entry.grid(row=2, column=1, pady=5)

alt_label = ttk.Label(frame, text="Altitude:")
alt_label.grid(row=3, column=0, sticky="w", pady=5)
alt_entry = ttk.Entry(frame)
alt_entry.grid(row=3, column=1, pady=5)

submit_button = ttk.Button(frame, text="Check Signal", command=process_input)
submit_button.grid(row=4, column=0, columnspan=2, pady=10)

map_button = ttk.Button(frame, text="View GPS Map", command=generate_map)
map_button.grid(row=5, column=0, columnspan=2, pady=10)

result_label = ttk.Label(frame, text="", font=("Arial", 12, "bold"))
result_label.grid(row=6, column=0, columnspan=2, pady=10)

root.mainloop()
