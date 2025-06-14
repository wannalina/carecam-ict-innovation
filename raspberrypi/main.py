import os
os.environ["XDG_RUNTIME_DIR"] = "/tmp/runtime-user"
os.environ['SDL_AUDIODRIVER'] = 'dummy'
import pygame
import time

from button_module import ButtonHandler
from camera_module import take_photo
from cloud_module import upload_photo, get_patient_data
from display_module import render_patient_data

# Inizializzazione Pygame
pygame.init()
screen = pygame.display.set_mode((800, 480))
pygame.display.set_caption('Patient Data')

# Variabile globale
current_patient_data = None
should_render = False  # Flag per dire se dobbiamo renderizzare

def handle_photo():
    global current_patient_data, should_render
    print("[INFO] Scatto foto...")
    image_path = take_photo()
    print(f"[INFO] Foto salvata in: {image_path}")

    print("[INFO] Invio foto al cloud finto...")
    if upload_photo(image_path):
        print("[INFO] Recupero dati paziente...")
        current_patient_data = get_patient_data()
        print(f"[DEBUG] Dati paziente ricevuti: {current_patient_data}")
        should_render = True
    else:
        print("[ERRORE] Upload fallito. Nessun dato mostrato.")

def handle_scroll_up():
    print("[INFO] Pulsante 'Scroll Up' premuto (non fa nulla per ora)")

def handle_scroll_down():
    print("[INFO] Pulsante 'Scroll Down' premuto (non fa nulla per ora)")

if __name__ == "__main__":
    buttons = ButtonHandler(
        photo_callback=handle_photo,
        scroll_up_callback=handle_scroll_up,
        scroll_down_callback=handle_scroll_down
    )

    print("[INFO] Sistema attivo. Premi un pulsante per iniziare...")

    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise KeyboardInterrupt

            if should_render and current_patient_data:
                from display_module import render_patient_data
                print("[DEBUG] Sto per chiamare render_patient_data")
                render_patient_data(screen, current_patient_data)
                pygame.display.flip()
                should_render = False

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("[INFO] Uscita dal programma.")
    finally:
        pygame.quit()
