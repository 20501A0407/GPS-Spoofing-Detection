📡 GPS Spoofing Detection System  

A **real-time GPS spoofing detection** system using **machine learning, cryptographic authentication, and map visualization**.  

Features  
 *ML-based Spoofing Detection** – Detects fraudulent GPS signals with high accuracy.  
 *Cryptographic Authentication** – Uses digital signatures to verify GPS data integrity.  
 *Real-time GPS Tracking** – Visualizes signals on an interactive **map** using Folium.  
 *Data Logging** – Stores all signals in an SQLite database for analysis.  
 *User-friendly GUI** – Built with Tkinter for easy interaction.  

🛠️ Installation  

**1️⃣ Clone Repository**  
```sh
git clone https://github.com/20501A0407/GPS-Spoofing-Detection.git
cd GPS-Spoofing-Detection
2️⃣ Install Dependencies
sh
Copy
Edit
pip install -r requirements.txt
3️⃣ Run the Application
sh
Copy
Edit
python gps_gui.py
📊 How It Works
Captures GPS Signals (simulated or real).

Verifies Authenticity using cryptographic methods.

ML Model Classifies signals as authentic or spoofed.

Displays Real-time Map & Logs Events in a database.

🎯 Future Improvements
🔹 Advanced ML models (Deep Learning)
🔹 Integration with live GPS receivers
🔹 Mobile app version

📝 License
This project is open-source under the MIT License.
