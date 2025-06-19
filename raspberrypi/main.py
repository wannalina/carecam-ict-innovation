import os
os.environ["XDG_RUNTIME_DIR"] = "/tmp/runtime-user"
os.environ['SDL_AUDIODRIVER'] = 'dummy'

import pygame
import time
import asyncio
import sys

from utils.button_module import ButtonHandler
from services.camera_module import take_photo
from utils.cloud_module import upload_photo, get_patient_data as get_cloud_patient_data
from ui.display_module import render_patient_data, render_start_instructions, render_bluetooth_instructions, reset_display
from services.bluetooth_module import discover_devices, select_and_connect_device
# from utils.cloud_module import post_to_nodered

# setup PyGame
pygame.init()
screen = pygame.display.set_mode((800, 480))
pygame.display.set_caption('Patient Data')

# track state
current_patient_data = None
should_render = False
reset_render = False
render_start = True
render_bluetooth_instruct = False
devices = []



# function to check if patient data should be rendered
def check_render_patient_data():
    global should_render, reset_render, current_patient_data, render_start, render_bluetooth_instruct, devices
    try:
        # clear screen and reset display before rendering new data
        if reset_render:
            reset_render = reset_display(screen)

        # render start instructions
        if render_start:
            current_patient_data = None
            render_start = False
            render_start_instructions(screen)
            time.sleep(0.1)

        # render bluetooth instructions and discovered devices
        if render_bluetooth_instruct:
            render_bluetooth_instruct = render_bluetooth_instructions(
                                            screen, 
                                            devices, 
                                            scroll_down_callback=buttons.get_scroll_down_trigger,
                                            confirm_callback=buttons.get_confirm_trigger,
                                            back_callback=buttons.get_back_trigger
                                         )
            time.sleep(0.1)

        # render patient data if exists and allowed
        if should_render and current_patient_data:
            print("yes==")
            render_patient_data(screen, current_patient_data)
            # post_to_nodered(current_patient_data)
            should_render = False

    except Exception as e:
        print(f"Error rendering patient data: {e}")
        return

# function to convert data from bluetooth into correct datatype
def build_patient_json(patient):
    patient = {
        "First Name": patient.get("First Name", ""),
        "Last Name": patient.get("Last Name", ""),
        "Image": "",  # placeholder
        "Date of Birth": patient.get("Date of Birth", ""),
        "Sex": patient.get("Sex", ""),
        "Conditions": patient.get("Conditions", "").split(',') if patient.get("Conditions", "") else [],
        "Medication": patient.get("Medication", "").split(',') if patient.get("Medication", "") else [],
        "Allergies": patient.get("Allergies", "").split(',') if patient.get("Allergies", "") else [],
        "Emergency Contact": patient.get("Emergency Contact", "").split(',') if patient.get("Emergency Contact", "") else []
    }
    return patient, True

# photo button handlers
def handle_photo():
    global current_patient_data, should_render, reset_render, render_start
    render_start = False
    reset_render = True
    current_patient_data = None # reset patient data

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
    time.sleep(0.1)

# function to return to main instructions
def handle_back_to_start():
    global render_start
    print("[INFO] Back to start pressed.")
    render_start = True

# function to scroll down using buttons
def handle_scroll_down():
    print("[INFO] Scroll Down pressed.")

# function to select and pair bluetooth devices
def handle_bluetooth_pairing():
    try:
        global current_patient_data, reset_render, render_start, render_bluetooth_instruct, devices, should_render
        render_start = False
        current_patient_data = None # reset patient data

        print("[BLUETOOTH] Discovering Bluetooth devices...")
        devices, render_bluetooth_instruct = asyncio.run(discover_devices())

        if not devices:
            print("[BLUETOOTH] No devices found.")
            return

        patient_data, render_bluetooth_instruct = asyncio.run(select_and_connect_device(
                                devices,
                                scroll_down_callback=buttons.get_scroll_down_trigger_ble,
                                confirm_callback=buttons.get_confirm_trigger_ble,
                                back_callback=buttons.get_back_trigger_ble
                            ))

        if patient_data:
            reset_render = True
            current_patient_data, should_render = build_patient_json(patient_data)
        else: 
            current_patient_data = None

        time.sleep(0.1)
        
    except Exception as e:
        print(f"[BLUETOOTH] Error pairing device: {e}")

# function to confirm bluetooth pairing and fetch patient data
def handle_bluetooth_confirm():
    print("[BLUETOOTH] Confirm pressed")

if __name__ == "__main__":
    try:
        # define camera buttons
        buttons = ButtonHandler(
            photo_callback=handle_photo,
            back_callback=handle_back_to_start,
            scroll_down_callback=handle_scroll_down,
            bluetooth_pairing_callback=handle_bluetooth_pairing,
            bluetooth_confirm_callback=handle_bluetooth_confirm
        )

        print("[SYSTEM] System initialized. Listening for events...")
        
        while True:
            check_render_patient_data()
        
    except KeyboardInterrupt:
        print("[SYSTEM] Shutting down...")
    except Exception as e: 
        print(f"Error in main: {e}")
    finally:
        pygame.quit()
        sys.exit(0)
