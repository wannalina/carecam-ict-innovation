import os
os.environ["XDG_RUNTIME_DIR"] = "/tmp/runtime-user"
os.environ['SDL_AUDIODRIVER'] = 'dummy'

import pygame
import time
import threading
import asyncio
import RPi.GPIO as GPIO

from utils.button_module import ButtonHandler
from services.camera_module import take_photo
from utils.cloud_module import upload_photo, get_patient_data as get_cloud_patient_data
from utils.display_module import render_patient_data
from services.bluetooth_module import (
    button_press_action,
    discover_devices,
    select_and_connect_device,
    get_services_on_device
)

# bluetoth GPIO pins
BLUETOOTH_BUTTON_PIN = 17
SELECT_BUTTON_PIN = 27
BLUETOOTH_LED_PIN = 12

# setup bluetooth GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(BLUETOOTH_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SELECT_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BLUETOOTH_LED_PIN, GPIO.OUT)

# setup PyGame
pygame.init()
screen = pygame.display.set_mode((800, 480))
pygame.display.set_caption('Patient Data')

# track state
current_patient_data = None
should_render = False
bluetooth_button_index = 1


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

'''
# function to scroll up using buttons
def handle_scroll_up():
    print("[INFO] Scroll Up pressed.")

# function to scroll down using buttons
def handle_scroll_down():
    print("[INFO] Scroll Down pressed.")
'''

# bluetooth thread
def bluetooth_loop():
    try:
        global bluetooth_button_index, current_patient_data, should_render
        while True:
            button_state = GPIO.input(BLUETOOTH_BUTTON_PIN)
            bluetooth_button_index = button_press_action(button_state, BLUETOOTH_LED_PIN, bluetooth_button_index)

            if bluetooth_button_index % 2 == 0:
                print("[BLUETOOTH] Starting discovery...")
                devices = asyncio.run(discover_devices())

                if not devices:
                    print("[BLUETOOTH] No devices found.")
                    continue

                device = asyncio.run(select_and_connect_device(
                    devices,
                    SELECT_BUTTON_PIN,
                    BLUETOOTH_BUTTON_PIN,
                    BLUETOOTH_LED_PIN
                ))

                if device:
                    print("[BLUETOOTH] Fetching patient data from BLE...")
                    patient_data = asyncio.run(get_services_on_device(device))
                    if patient_data:
                        current_patient_data = patient_data
                        should_render = True
            time.sleep(0.1)

    except Exception as e:
        print(f"[BLUETOOTH] Error: {e}")
    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    try:
        # define camera buttons
        buttons = ButtonHandler(
            photo_callback=handle_photo,
            scroll_up_callback=handle_scroll_up,
            scroll_down_callback=handle_scroll_down
        )

        print("[SYSTEM] System initialized. Listening for events...")

        # start bluetooth in another thread
        bluetooth_thread = threading.Thread(target=bluetooth_loop, daemon=True)
        bluetooth_thread.start()

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
        GPIO.cleanup()
        pygame.quit()
