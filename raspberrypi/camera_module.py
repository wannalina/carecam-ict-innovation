import subprocess
import os
from datetime import datetime

PHOTO_DIR = "photos"

def take_photo():
        # Create the directory if it doesn't exist
        if not os.path.exists(PHOTO_DIR):
                os.makedirs(PHOTO_DIR)

        # File name with timestamp
        filename = datetime.now().strftime("%Y%m%d_%H%M%S.jpg")
        filepath = os.path.join(PHOTO_DIR, filename)

        #fswebcam command
        command = ["fswebcam", "--no-banner", "-r", "640x480", filepath]

        try:
                subprocess.run(command, check=True)
                print(f"[Camera] Picture saved in {filepath}")
                return filepath
        except subprocess.CalledProcessError:
                print("[Camera] Errror while taking the picture.")
                return None
