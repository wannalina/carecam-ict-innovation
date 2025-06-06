# import libraries
import RPi.GPIO as GPIO
import time
import asyncio
from bleak import BleakScanner, BleakClient # TEST

# import functions from libs
from bluetooth_module.bluetooth import discover_devices, select_and_connect_device

# pin config
BLUETOOTH_BUTTON_PIN = 17	# corresponds to physical pin 11
SELECT_BUTTON_PIN = 27       # corresponds to physical pin 13
BLUETOOTH_LED_PIN = 12		# corresponds to phsyical pin 32

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(BLUETOOTH_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SELECT_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BLUETOOTH_LED_PIN, GPIO.OUT)

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

# function to control application and run main program loop
async def main():
    devices = []
    button_index = 1    # even numbers "on"; odd numbers "off"
    scroll_index = 0
    last_scroll_index = 0
    last_selected_state = GPIO.input(SELECT_BUTTON_PIN)
    last_confirm_state = GPIO.input(BLUETOOTH_BUTTON_PIN)
    try:
        while True:
            # get state of bluetooth button
            bluetooth_button_state = GPIO.input(BLUETOOTH_BUTTON_PIN)
            button_index = button_press_action(bluetooth_button_state, BLUETOOTH_LED_PIN, button_index)

            # if bluetooth button pressed, begin device discovery
            if button_index % 2 == 0:
                devices = await discover_devices()

                ''' TEST '''
                #asyncio.run(select_and_connect_device(devices, SELECT_BUTTON_PIN, BLUETOOTH_BUTTON_PIN))
                if not devices:
                    print("No devices to pair. Please check Bluetooth settings.")
                    return

                print("Use the button to 'scroll' through the list of devices. Select using the original button.")

                while True:
                    device = devices[scroll_index]  # selected device
                    print(f"Currently selected device: {device.name} with address {device.address}")

                    # wait for button press
                    while True: 
                        select_state = GPIO.input(SELECT_BUTTON_PIN)   # select button state
                        confirm_state = GPIO.input(BLUETOOTH_BUTTON_PIN) # confirm button state

                        scroll_index = button_press_action(select_state, BLUETOOTH_LED_PIN, scroll_index)
                        # select button pressed
                        if scroll_index != last_scroll_index:
                            print(f"Scroll button pressed {scroll_index} times.")
                            device = devices[scroll_index]
                            last_scroll_index = scroll_index
                            break

                        # confirm pressed
                        if confirm_state == GPIO.LOW and last_confirm_state == GPIO.HIGH:
                            print(f"Attempting connection to '{device.name}'...")
                            try: 
                                async with BleakClient(device.address) as client:
                                    print("Device connected via Bluetooth successfully!")
                                    await asyncio.sleep(5)  #TODO: retrieve app data here
                                return
                            except Exception as e:
                                print(f"Connection failed: {e}")
                                return

                        # reset i/o
                        last_selected_state = select_state
                        last_confirm_state = confirm_state
                        time.sleep(0.1)

                ''' TEST END '''
            else:
                continue
            print(f"Discovered devices: {devices}")
            print(f"Button state: {bluetooth_button_state}, {button_index}")
            time.sleep(0.1)

    except Exception as e:
        print(f"Error running main application loop: {e}")
    finally:
        GPIO.cleanup()


asyncio.run(main())
