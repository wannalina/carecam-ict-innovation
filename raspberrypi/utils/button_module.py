import threading
from gpiozero import Button, LED
from signal import pause
from raspberrypi.services.camera_module import take_photo

class ButtonHandler:
    def __init__(self, photo_callback=None, scroll_up_callback=None, scroll_down_callback=None, 
                bluetooth_pairing_callback=None, bluetooth_confirm_callback=None):
        self.photo_button = Button(4, bounce_time=0.5)
        self.scroll_up_button = Button(22, bounce_time=0.5)
        self.scroll_down_button = Button(27, bounce_time=0.5)
        self.bluetooth_button = Button(17, bounce_time=0.5)

        self.led_photo = LED(21)
        self.led_scroll = LED(20)
        self.led_bluetooth = LED(12)

        self.photo_callback = photo_callback
        self.scroll_up_callback = scroll_up_callback
        self.scroll_down_callback = scroll_down_callback
        self.bluetooth_pairing_callback = bluetooth_pairing_callback
        self.bluetooth_confirm_callback = bluetooth_confirm_callback

        self.photo_button.when_pressed = self.handle_photo_press
        self.scroll_up_button.when_pressed = self.handle_scroll_up
        self.scroll_down_button.when_pressed = self.handle_scroll_down
        self.bluetooth_button.when_pressed = self.handle_bluetooth_press

        # bluetooth state
        self.bluetooth_button_index = 0

    def handle_photo_press(self):
        print("[Button] Foto richiesta")
        self.led_photo.blink(on_time=0.2, off_time=0.2, n=2)
        if self.photo_callback:
            self.photo_callback()

    def handle_scroll_up(self):
        print("[Button] Scroll su")
        self.led_scroll.blink(on_time=0.1, off_time=0.1, n=1)
        if self.scroll_up_callback:
            self.scroll_up_callback()

    def handle_scroll_down(self):
        print("[Button] Scroll giù")
        self.led_scroll.blink(on_time=0.1, off_time=0.1, n=1)
        if self.scroll_down_callback:
            self.scroll_down_callback()

    def handle_bluetooth_press(self):
        print("[Button] Bluetooth pairing")
        self.led_bluetooth.blink(on_time=0.2, off_time=0.2, n=2)

        if self.bluetooth_button_index % 2 == 0 and self.bluetooth_confirm_callback:
            print("[BLUETOOTH] Start pairing...")
            thread = threading.Thread(target=self.bluetooth_pairing_callback, args=self.bluetooth_led,)
            thread.start()
        elif self.bluetooth_button_index & 2 != 0 and self.bluetooth_pairing_callback:
            print("[BLUETOOTH] Confirm device pairing...")
            self.bluetooth_confirm_callback()
        self.bluetooth_button_index += 1

    def run(self):
        print("[Button] In ascolto dei pulsanti...")
        pause()

# Per test standalone
if __name__ == "__main__":
    handler = ButtonHandler()
    handler.run()
