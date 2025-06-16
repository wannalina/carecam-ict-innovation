import threading
from gpiozero import Button, LED
from signal import pause
from services.camera_module import take_photo

class ButtonHandler:
    def __init__(self, photo_callback=None, scroll_up_callback=None, scroll_down_callback=None, 
                bluetooth_pairing_callback=None, bluetooth_confirm_callback=None):

        # button wiring
        self.photo_button = Button(4, bounce_time=0.5)
        self.scroll_up_button = Button(22, bounce_time=0.5)
        self.scroll_down_button = Button(27, bounce_time=0.5)
        self.bluetooth_button = Button(17, bounce_time=0.5)

        # LED light wiring
        self.led_photo = LED(21)
        self.led_scroll = LED(20)
        self.led_bluetooth = LED(12)

        # callbacks
        self.photo_callback = photo_callback
        self.scroll_up_callback = scroll_up_callback
        self.scroll_down_callback = scroll_down_callback
        self.bluetooth_pairing_callback = bluetooth_pairing_callback
        self.bluetooth_confirm_callback = bluetooth_confirm_callback

        # state flags
        self.bluetooth_button_index = 1
        self._scroll_up_triggered = False
        self._scroll_down_triggered = False
        self._confirm_triggered = False

        # event binding
        self.photo_button.when_pressed = self.handle_photo_press
        self.scroll_up_button.when_pressed = self.handle_scroll_up
        self.scroll_down_button.when_pressed = self.handle_scroll_down
        self.bluetooth_button.when_pressed = self.handle_bluetooth_press

    def handle_photo_press(self):
        print("[Button] Foto richiesta")
        self.led_photo.blink(on_time=0.2, off_time=0.2, n=2)
        if self.photo_callback:
            self.photo_callback()

    def handle_scroll_up(self):
        print("[Button] Scroll su")
        self._scroll_up_triggered = True
        self.led_scroll.blink(on_time=0.1, off_time=0.1, n=1)
        if self.scroll_up_callback:
            self.scroll_up_callback()

    def handle_scroll_down(self):
        print("[Button] Scroll giù")
        self._scroll_down_triggered = True
        self.led_scroll.blink(on_time=0.1, off_time=0.1, n=1)
        if self.scroll_down_callback:
            self.scroll_down_callback()


    def handle_bluetooth_press(self):
        self.led_bluetooth.blink(on_time=0.2, off_time=0.2, n=2)

        if self.bluetooth_button_index % 2 != 0 and self.bluetooth_pairing_callback:
            print("[BLUETOOTH] Start device discovery...")
            self.led_bluetooth.blink(on_time=0.1, off_time=0.1, n=1)
            thread = threading.Thread(target=self.bluetooth_pairing_callback)
            thread.start()
        if self.bluetooth_button_index % 2 == 0 and self.bluetooth_confirm_callback:
            print("[BLUETOOTH] Confirm device pairing...")
            self._confrim_triggered = True
            self.led_bluetooth.blink(on_time=0.2, off_time=0.2, n=2)
            self.bluetooth_confirm_callback()
        self.bluetooth_button_index += 1
        print(f"Bluetooth button index: {self.bluetooth_button_index}")

    def get_scroll_up_trigger(self):
        triggered = self._scroll_up_triggered
        self._scroll_up_triggered = False
        return triggered

    def get_scroll_down_trigger(self):
        triggered = self._scroll_down_triggered
        self._scroll_down_triggered = False
        return triggered

    def get_confirm_trigger(self):
        triggered = self._confirm_triggered
        self._confirm_triggered = False
        return triggered

    def run(self):
        print("[Button] In ascolto dei pulsanti...")
        pause()

# Per test standalone
if __name__ == "__main__":
    handler = ButtonHandler()
    handler.run()
