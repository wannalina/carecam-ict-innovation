import subprocess
import os
from picamera2 import Picamera2
from time import sleep
from datetime import datetime

PHOTO_DIR = "/photos"
picam = Picamera2()     # initialize picam

def take_photo():
        # Create the directory if it doesn't exist
        if not os.path.exists(PHOTO_DIR):
                os.makedirs(PHOTO_DIR)

        # File name with timestamp
        filename = datetime.now().strftime("%Y%m%d_%H%M%S.jpg")
        filepath = os.path.join(PHOTO_DIR, filename)

        try:
                picam.start()
                sleep(2)
                picam.capture_file(filepath)    # take picture
                print(f"[Camera] Picture saved in {filepath}")
                return filepath
        except subprocess.CalledProcessError:
                print("[Camera] Error while taking the picture.")
                return None
