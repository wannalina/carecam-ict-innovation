import os
os.environ["XDG_RUNTIME_DIR"] = "/tmp/runtime-user"
os.environ['SDL_AUDIODRIVER'] = 'dummy'

import pygame
import time
import asyncio

from utils.button_module import ButtonHandler
from services.camera_module import take_photo
from utils.cloud_module import upload_photo, get_patient_data as get_cloud_patient_data
from utils.display_module import render_patient_data
from services.bluetooth_module import (
    discover_devices,
    select_and_connect_device,
    get_services_on_device
)

# setup PyGame
pygame.init()
screen = pygame.display.set_mode((800, 480))
pygame.display.set_caption('Patient Data')

# track state
current_patient_data = None
should_render = False
device = {}


# photo button handlers
def handle_photo():
    global current_patient_data, should_render
    print("[INFO] Taking photo...")
    image_path = take_photo()
    if not image_path:
        print("[ERROR] Photo capture failed.")
        return

    print(f"[INFO] Photo saved at {image_path}, uploading...")
    if upload_photo(image_path):
        current_patient_data = get_cloud_patient_data()
        should_render = True
    else:
        print("[ERROR] Upload failed.")


# function to scroll up using buttons
def handle_scroll_up():
    print("[INFO] Scroll Up pressed.")

# function to scroll down using buttons
def handle_scroll_down():
    print("[INFO] Scroll Down pressed.")

# function to pair/confirm Bluetooth
def handle_bluetooth():
    print("[INFO] Bluetooth pair/confirm pressed.")

# function to select and pair bluetooth devices
def handle_bluetooth_pairing():
    try:
        global device

        print("[BLUETOOTH] Discovering Bluetooth devices...")
        devices = asyncio.run(discover_devices())

        if not devices:
            print("[BLUETOOTH] No devices found.")
            return

        device = asyncio.run(select_and_connect_device(devices, andle_scroll_down, handle_bluetooth))

    except Exception as e:
        print(f"[BLUETOOTH] Error pairing device: {e}")

# function to confirm bluetooth pairing and fetch patient data
def handle_bluetooth_confirm():
    global device, current_patient_data, should_render
    try:
        if device: 
            print("[BLUETOOTH] Fetching patient data from device...")
            patient_data = asyncio.run(get_services_on_device(device))

            if patient_data:
                current_patient_data = patient_data
                should_render = True
    except Exception as e:
        print(f"[BLUETOOTH] Error confirming: {e}")


if __name__ == "__main__":
    try:
        # define camera buttons
        buttons = ButtonHandler(
            photo_callback=handle_photo,
            scroll_up_callback=handle_scroll_up,
            scroll_down_callback=handle_scroll_down,
            bluetooth_pairing_callback=handle_bluetooth_pairing,
            bluetooth_confirm_callback=handle_bluetooth_confirm
        )

        print("[SYSTEM] System initialized. Listening for events...")

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise KeyboardInterrupt

            # render patient data if exists and allowed
            if should_render and current_patient_data:
                render_patient_data(screen, current_patient_data)
                should_render = False

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("[SYSTEM] Shutting down...")
    except Exception as e: 
        print(f"Error in main: {e}")
    finally:
        pygame.quit()
