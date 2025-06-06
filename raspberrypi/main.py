# import libraries
import RPi.GPIO as GPIO
import time
import asyncio

# import functions from libs
from bluetooth_module.bluetooth import discover_devices, select_and_connect_device

# pin config
BLUETOOTH_BUTTON_PIN = 17	# corresponds to physical pin 11
BLUETOOTH_LED_PIN = 12		# corresponds to phsyical pin 32
SELECT_BUTTON_PIN = 2       # corresponds to physical pin 3

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(BLUETOOTH_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SELECT_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BLUETOOTH_LED_PIN, GPIO.OUT)

# function to listen to button press; returns int
def button_press_action(button_state, output_pin, button_index):
    try:
        if (button_state == GPIO.HIGH):
            # button pressed "on" or "off"
            GPIO.output(output_pin, GPIO.HIGH)
            button_index += 1   # switch button status
            return button_index
        else:
            # button not pressed
            GPIO.output(output_pin, GPIO.LOW)
            return button_index
        time.sleep(0.2)
    except Exception as e:
        print(f"Error reading button input: {e}")

# function to control application and run main program loop
def main():
    devices = []
    button_index = 0    # even numbers "on"; odd numbers "off"
    try:
        while True:
            # get state of bluetooth button
            bluetooth_button_state = GPIO.input(BLUETOOTH_BUTTON_PIN)
            is_bluetooth_on = button_press_action(bluetooth_button_state, BLUETOOTH_LED_PIN, button_index)

            # if bluetooth button pressed, begin device discovery
            if is_bluetooth_on:
                devices = asyncio.run(discover_devices())
                asyncio.run(select_and_connect_device(devices, SELECT_BUTTON_PIN, BLUETOOTH_BUTTON_PIN))
            else:
                continue
            print(f"Discovered devices: {devices}")
            time.sleep(0.5)

    except Exception as e:
        print(f"Error running main application loop: {e}")
    finally:
        GPIO.cleanup()

main()
