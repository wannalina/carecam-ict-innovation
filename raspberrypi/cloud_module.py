import os
import shutil
import json

FAKE_CLOUD_DIR = "fake_cloud"
PATIENT_DATA_FILE = os.path.join(FAKE_CLOUD_DIR, "patient_data.json")

def upload_photo(photo_path):
        if not os.path.exists(FAKE_CLOUD_DIR):
                os.makedirs(FAKE_CLOUD_DIR)

        dest_path = os.path.join(FAKE_CLOUD_DIR, os.path.basename(photo_path))
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
