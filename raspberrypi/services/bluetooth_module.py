# import libs
from bleak import BleakScanner, BleakClient 	# bleak used for BLE / ideal for modern phones
import asyncio
import RPi.GPIO as GPIO
import time

# service UUID of the EmergencyID app
APP_UUID = "00001234-0000-1000-8000-00805f9b34fb"
CHARACTERISTIC_INDEX = {
                            "00002a8a-0000-1000-8000-00805f9b34fb": "First Name", 
                            "00002a90-0000-1000-8000-00805f9b34fb": "Last Name", 
                            "00002a85-0000-1000-8000-00805f9b34fb": "Date of Birth",
                            "00002a8c-0000-1000-8000-00805f9b34fb": "Sex",
                            "00012a1e-0000-1000-8000-00805f9b34fb": "Allergies",
                            "00002bff-0000-1020-8000-00805f9b34fb": "Medication",
                            "00112b35-0000-1000-8000-00805f9b34fb": "Cholesterol Level"
                        }

# function to listen to button press; returns int
def button_press_action(button_state, output_pin, button_index):
    try:
        if button_state == GPIO.HIGH:
            # button pressed "on" or "off"
            GPIO.output(output_pin, GPIO.HIGH)
            button_index += 1   # switch button status
            return button_index
        else:
            # button not pressed
            GPIO.output(output_pin, GPIO.LOW)
            return button_index
        time.sleep(0.5)
        GPIO.output(BLUETOOTH_LED_PIN, GPIO.LOW)   # turn indicator led off for testing
    except Exception as e:
        print(f"Error reading button input: {e}")

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
async def select_and_connect_device(devices, select_pin, confirm_pin, led_pin):
    isTrue = True
    scroll_index = 0
    last_scroll_index = 0
    last_selected_state = GPIO.input(select_pin)
    last_confirm_state = GPIO.input(confirm_pin)
    try:
        if not devices:
            print("No devices to pair. Please check Bluetooth settings.")
            return

        print("Use the button to 'scroll' through the list of devices. Select using the original button.")

        while isTrue:
            device = devices[scroll_index]  # selected device
            print(f"Currently selected device: {device.name} with address {device.address}")

            # wait for button press
            while isTrue: 
                select_state = GPIO.input(select_pin)   # select button state
                confirm_state = GPIO.input(confirm_pin) # confirm button state

                scroll_index = button_press_action(select_state, led_pin, scroll_index)

                # check if scroll index out of range
                if scroll_index == len(devices):
                    scroll_index = 0
                    last_scroll_index = -1

                # select button pressed
                if scroll_index != last_scroll_index:
                    device = devices[scroll_index]
                    print(f"Currently selected device: {device.name} with address {device.address}")
                    last_scroll_index = scroll_index
                    time.sleep(0.2)

                # confirm pressed
                elif confirm_state == GPIO.LOW and last_confirm_state == GPIO.HIGH:
                    print(f"Attempting connection to '{device.name}'...")
                    try: 
                        async with BleakClient(device.address) as client:
                            print("Device connected via Bluetooth successfully!")

                            if device:
                                patient_characteristics = await get_services_on_device(device)

                        isTrue = False  # break all loops
                        return device
                    except Exception as e:
                        print(f"Connection failed: {e}")
                        return

                # reset i/o
                last_selected_state = select_state
                last_confirm_state = confirm_state

    except Exception as e:
        print(f"Error selecting and connecting to device: {e}")
        return None

# function to retrieve services running on the connected device
async def get_services_on_device(device):
    patient_characteristics = {}
    try:
        async with BleakClient(device.address) as client:
            # check if devices are connected
            if not client.is_connected:
                print("Error connecting to device.")
                return

            services = client.services

            # if no available services
            if not services:
                print("No services running on the device.")
                return

            # find EISI app service from services list
            for service in services:
                # if service UUID equals EmergencyID app
                if service.uuid == APP_UUID:
                    for characteristic in service.characteristics:
                        if "read" in characteristic.properties:
                            # retrieve patient data and add to dict
                            service_data = (await client.read_gatt_char(characteristic.uuid)).decode('utf-8')
                            patient_characteristics[CHARACTERISTIC_INDEX[characteristic.uuid]] = service_data
                    print(f"Patient: {patient_characteristics}")
                    return patient_characteristics
            return None
                
    except Exception as e:
        print(f"Error retrieving services from device: {e}")
        return
