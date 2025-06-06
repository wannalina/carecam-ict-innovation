from bleak import BleakScanner 	# bleak used for BLE / ideal for modern phones

# function to discover bluetooth devices
async def discover_devices():
    try:
        devices = await BleakScanner.discover()
        for device in devices:
            print(f"Device {device.name} found with address: {device.address}")
    except Exception as e:
        print(f"Error in device discovery: {e}")
