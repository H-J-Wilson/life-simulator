# Planes Project Setup

## Requirements
* Python 3.10 or later

## Installation & Setup

1. **Download project files** into a folder and **unzip** them.
2. Open your terminal or command line and **change directory (`cd`)** to the project folder.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the server:
   ```bash
   python main.py
   ```

## How to Find Your IP Address

To access the server from other devices on your home network, find your local IP address:
* **Windows:** Open Command Prompt and type `ipconfig` (look for IPv4 Address).
* **Mac / Linux:** Open Terminal and type `hostname -I` or `ip4`.

Open your web browser and navigate to: `http://<your_local_ip>:8000`
