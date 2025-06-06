# import libraries
import RPi.GPIO as GPIO
import time
import asyncio

# import functions from libs
from bluetooth_module.bluetooth import discover_devices

# pin config
BLUETOOTH_BUTTON_PIN = 17	# corresponds to physical pin 11
BLUETOOTH_LED_PIN = 12		# correpsonds to phsyical pin 32

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(BLUETOOTH_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BLUETOOTH_LED_PIN, GPIO.OUT)

# function to listen to button press; returns boolean
def button_press_action(button_state, output_pin):
    try:
        if button_state == GPIO.HIGH:
            # if button pressed turn on LED and return True
            print("Button pressed.")
            GPIO.output(output_pin, GPIO.HIGH)
            return True
        else:
            # if button released turn off LED and return False
            print("Button released.")
            GPIO.output(output_pin, GPIO.LOW)
            return False
        time.sleep(0.1)
    except Exception as e:
        print(f"Error reading button input: {e}")

# function to control application and run main program loop
def main():
    try:
        while True:
            # get state of bluetooth button
            bluetooth_button_state = GPIO.input(BLUETOOTH_BUTTON_PIN)
            is_bluetooth_on = button_press_action(bluetooth_button_state, BLUETOOTH_LED_PIN)

            # if bluetooth button pressed, begin device discovery
            if is_bluetooth_on:
                asyncio.run(discover_devices())		# discover bluetooth devices
            else:
                continue

    except Exception as e:
        print(f"Error running main application loop: {e}")
    finally:
        GPIO.cleanup()

main()
