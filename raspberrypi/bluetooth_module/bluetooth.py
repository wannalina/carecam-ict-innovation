# import libs
from bleak import BleakScanner, BleakClient 	# bleak used for BLE / ideal for modern phones
import asyncio
import RPi.GPIO as GPIO
import time

# function to discover bluetooth devices
async def discover_devices():
    try:
        devices = await BleakScanner.discover()
        for device in devices:
            print(f"Device {device.name} found with address: {device.address}")
        return devices
    except Exception as e:
        print(f"Error in device discovery: {e}")
        return []

# function to select and connect device
async def select_and_connect_device(devices, select_pin, confirm_pin):
    scroll_index = 0
    last_selected_state = GPIO.input(select_pin)
    last_confirm_state = GPIO.input(confirm_pin)
    try:
        if not devices:
            print("No devices to pair. Please check Bluetooth settings.")
            return

        print("Use the button to 'scroll' through the list of devices. Select using the original button.")

        while True:
            device = devices[scroll_index]  # selected device
            print(f"Selected device: {device.name} with address {device.address}")

            # wait for button press
            while True: 
                select_state = GPIO.input(select_pin)   # select button state
                confirm_state = GPIO.input(confirm_pin) # confirm button state

                # select button pressed
                if select_state == GPIO.LOW and last_selected_state == GPIO.HIGH:
                    scroll_index = (scroll_index + 1) % len(devices)    #
                    break

                # confirm pressed
                if confirm_state == GPIO.LOW and last_confirm_state == GPIO.HIGH:
                    print(f"Attempting connection to '{device.name}'...")
                    try: 
                        async with BleakClient(device.address) as client:
                            print("Device connected via Bluetooth successfully!")
                            await asyncio.sleep(2)  #TODO: retrieve app data here
                        return
                    except Exception as e:
                        print(f"Connection failed: {e}")
                        return

                # reset i/o
                last_selected_state = select_state
                last_confirm_state = confirm_state
                time.sleep(0.5)

    except Exception as e:
        print(f"Error selecting and connecting to device: {e}")
        return None
