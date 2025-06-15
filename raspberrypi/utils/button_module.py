from gpiozero import Button, LED
from signal import pause
from raspberrypi.services.camera_module import take_photo

class ButtonHandler:
    def __init__(self, photo_callback=None, scroll_up_callback=None, scroll_down_callback=None):
        self.photo_button = Button(4, bounce_time=0.5)
        self.scroll_up_button = Button(22, bounce_time=0.5)
        self.scroll_down_button = Button(27, bounce_time=0.5)

        self.led_photo = LED(21)
        self.led_scroll = LED(20)

        self.photo_callback = photo_callback
        self.scroll_up_callback = scroll_up_callback
        self.scroll_down_callback = scroll_down_callback

        self.photo_button.when_pressed = self.handle_photo_press
        self.scroll_up_button.when_pressed = self.handle_scroll_up
        self.scroll_down_button.when_pressed = self.handle_scroll_down

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

    def run(self):
        print("[Button] In ascolto dei pulsanti...")
        pause()

# Per test standalone
if __name__ == "__main__":
    handler = ButtonHandler()
    handler.run()
