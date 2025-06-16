# import libs
from bleak import BleakScanner, BleakClient 	# bleak used for BLE / ideal for modern phones
import asyncio

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
'''
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
'''

# function to discover bluetooth devices
async def discover_devices():
    try:
        devices = await BleakScanner.discover()
        for device in devices:
            print(f"[BLUETOOTH] Device {device.name} found with address: {device.address}")
        return devices
    except Exception as e:
        print(f"Error in device discovery: {e}")
        return []

# function to select and connect device
async def select_and_connect_device(devices, scroll_down_callback, confirm_callback):
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

        if scroll:
            scroll_index = (scroll_index + 1) % len(devices)
            if scroll_index != last_scroll_index:
                selected_device = devices[scroll_index]
                print(f"[BLUETOOTH] Selected: {selected_device.name} at {selected_device.address}")
                last_scroll_index = scroll_index

        if confirm:
            try:
                async with BleakClient(selected_device.address) as client:
                    print(f"[BLUETOOTH] Connected to {selected_device.name}")
                    await get_services_on_device(selected_device)
                    selected = True
                    return selected_device
            except Exception as e:
                print(f"Connection failed: {e}")
                return None
        await asyncio.sleep(0.2)

# function to retrieve services running on the connected device
async def get_services_on_device(device):
    patient_characteristics = {}
    try:
        async with BleakClient(device.address) as client:
            if not client.is_connected:
                print("[BLUETOOTH] Not connected to device.")
                return

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
