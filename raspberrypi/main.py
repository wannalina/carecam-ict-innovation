# import libraries
import RPi.GPIO as GPIO
import time
import asyncio

# import functions from libs
from bluetooth_module.bluetooth import button_press_action, discover_devices, select_and_connect_device

# pin config
BLUETOOTH_BUTTON_PIN = 17	# corresponds to physical pin 11
SELECT_BUTTON_PIN = 27       # corresponds to physical pin 13
BLUETOOTH_LED_PIN = 12		# corresponds to phsyical pin 32

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(BLUETOOTH_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SELECT_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BLUETOOTH_LED_PIN, GPIO.OUT)

# function to control application and run main program loop
def main():
    devices = []
    button_index = 1    # even numbers "on"; odd numbers "off"
    try:
        while True:
            # get state of bluetooth button
            bluetooth_button_state = GPIO.input(BLUETOOTH_BUTTON_PIN)
            button_index = button_press_action(bluetooth_button_state, BLUETOOTH_LED_PIN, button_index)

            # if bluetooth button pressed, begin device discovery
            if button_index % 2 == 0:
                devices = asyncio.run(discover_devices())

                # select device and pair 
                asyncio.run(select_and_connect_device(devices, 
                                                    SELECT_BUTTON_PIN, 
                                                    BLUETOOTH_BUTTON_PIN, 
                                                    BLUETOOTH_LED_PIN))
            else:
                continue
            time.sleep(0.1)

    except Exception as e:
        print(f"Error running main application loop: {e}")
    finally:
        GPIO.cleanup()


main()
