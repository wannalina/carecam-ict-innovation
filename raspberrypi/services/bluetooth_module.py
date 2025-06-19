# import libs
from bleak import BleakScanner, BleakClient 	# bleak used for BLE / ideal for modern phones
import asyncio
import time

# service UUID of the EmergencyID app
APP_UUID = "00001234-0000-1000-8000-00805f9b34fb"
CHARACTERISTIC_INDEX = {
                            "00002a8a-0000-1000-8000-00805f9b34fb": "First Name", 
                            "00002a90-0000-1000-8000-00805f9b34fb": "Last Name", 
                            "00002a85-0000-1000-8000-00805f9b34fb": "Date of Birth",
                            "00002a8c-0000-1000-8000-00805f9b34fb": "Sex",
                            "00002bc6-0000-1000-8000-00805f9b34fb": "Conditions",
                            "00012a1e-0000-1000-8000-00805f9b34fb": "Allergies",
                            "00002bff-0000-1020-8000-00805f9b34fb": "Medication",
                            "00112b35-0000-1000-8000-00805f9b34fb": "Cholesterol Level",
                            "00002b2d-0000-1000-8000-00805f9b34fb": "Emergency Contact"
                        }

# function to discover bluetooth devices
async def discover_devices():
    try:
        devices = await BleakScanner.discover()
        for device in devices:
            print(f"[BLUETOOTH] Device {device.name} found with address: {device.address}")
        return devices, True
    except Exception as e:
        print(f"Error in device discovery: {e}")
        return [], False

# function to select and connect device
async def select_and_connect_device(devices, scroll_down_callback, confirm_callback, back_callback):
    print("Use scroll down button to select device.")
    scroll_index = 0
    last_scroll_index = -1
    selected = False
    selected_device = None
    
    selected_device = devices[scroll_index]
    print(f"[BLUETOOTH] Selected: {selected_device.name} at {selected_device.address}")

    while not selected:
        scroll = scroll_down_callback()
        confirm = confirm_callback()
        back = back_callback()
        
        if back:
            selected = True
            selected_device = None
            return None, False

        if scroll:
            scroll_index = (scroll_index + 1) % len(devices)
            if scroll_index != last_scroll_index:
                selected_device = devices[scroll_index]
                print(f"[BLUETOOTH] Selected: {selected_device.name} at {selected_device.address}")
                last_scroll_index = scroll_index

        if confirm:
            selected = True
            print("Selected device:", selected_device)
            patient_data = await get_services_on_device(selected_device)
            return patient_data, False

    time.sleep(0.2)
    return None, False

# function to retrieve services running on the connected device
async def get_services_on_device(device):
    patient_characteristics = {}
    try:
        async with BleakClient(device.address) as client:
            print(f"[BLUETOOTH] Connected to {device.name}")
            # await get_services_on_device(selected_device)
            selected = True
            print(device)
        
            services = client.services

            if not services:
                print("[BLUETOOTH] No services available.")
                return

            # find EmergencyID app from services list
            for service in services:
                if service.uuid == APP_UUID:
                    for char in service.characteristics:
                        if "read" in char.properties:
                            # retrieve patient data and add to dict
                            service_data = (await client.read_gatt_char(char.uuid)).decode('utf-8')
                            patient_characteristics[CHARACTERISTIC_INDEX[char.uuid]] = service_data

                    print(f"[BLUETOOTH] Patient data: {patient_characteristics}")
                    return patient_characteristics
        return None

    except Exception as e:
        print(f"Error retrieving services: {e}")
        return None
