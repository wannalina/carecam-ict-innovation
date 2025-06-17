import os
import shutil
import json
import requests

FAKE_CLOUD_DIR = "../database/"
PHOTOS_DIR = "../database/photos/"
PATIENT_DATA_FILE = os.path.join(FAKE_CLOUD_DIR, "patient_data.json")
NODE_RED_URL = "http://localhost:1880"

def upload_photo(photo_path):
        if not os.path.exists(PHOTOS_DIR):
                os.makedirs(PHOTOS_DIR)

        dest_path = os.path.join(PHOTOS_DIR, os.path.basename(photo_path))
        try:
                shutil.copy(photo_path, dest_path)
                print(f"[Cloud] Picture sent to the cloud: {dest_path}")
                return True
        except Exception as e:
                print(f"[Cloud] Error while uploading: {e}")
                return False

def get_patient_data():
        try:
                with open(PATIENT_DATA_FILE, "r") as f:
                        data = json.load(f)
                        print("[Cloud] Patient data received")
                        return data
        except Exception as e:
                print(f"[Cloud] Error while recovering data: {e}")
                return {}

def post_to_nodered(patient_data):
        try:
                response = requests.post(f"{NODE_RED_URL}/patient-data", json=patient_data)
                if response.status_code == 200:
                        print("[Cloud] Data sent to Node-RED successfully")
                else:
                        print(f"[Cloud] Failed to send data to Node-RED: {response.status_code}")
                return
        except Exception as e:
                print(f"[Cloud] Error sending data to Node-RED: {e}")
                return
