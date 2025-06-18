import pygame

# define colors
BACKGROUND_COLOR = (245, 245, 245)
TEXT_COLOR = (30, 30, 30)
TITLE_COLOR = (0, 150, 230)
CARD_COLOR = (255, 255, 255)
BORDER_COLOR = (220, 220, 220)

# define fonts
pygame.font.init()  # assicurati che il font system sia inizializzato  
TITLE_FONT = pygame.font.Font(None, 30, bold=True)
TEXT_FONT = pygame.font.Font(None, 24, bold=True)  

# define component measurements
HEADER_BLOCK_DIM = (0, 0, 800, 40)
IMAGE_SIZE = (180, 140)
IMAGE_X = 570
IMAGE_Y = 50
START_X_LEFT = 20
START_X_RIGHT = 400
START_Y_TOP = 50
START_Y_MIDDLE = 205
START_Y_BOTTOM = 340
CARD_WIDTH = 370
CARD_HEIGHT = 120
SELECTED_DEV_X = 150
SELECTED_DEV_Y = 430

START_INSTRUCTIONS_CAMERA = [
    "To take a picture of the patient's face,", 
    "Press the 4th button from the right."
]

START_INSTRUCTIONS_BLUETOOTH = [
    "To activate Bluetooth pairing,",
    "Press the 3rd button from the right."
]

def render_start_instructions(screen):
    screen.fill(BACKGROUND_COLOR)

    def build_instructions(start_x, start_y, text, instruction_set):
        title_text = TITLE_FONT.render(text, True, TITLE_COLOR)
        screen.blit(title_text, (start_x + 40, start_y + 30))

        y_offset = start_y + 70
        for instruction in instruction_set:
            instruction_text = TEXT_FONT.render(instruction, True, TEXT_COLOR)
            screen.blit(instruction_text, (start_x, y_offset)) 
            y_offset += 40

    build_instructions(250, START_Y_TOP + 30, "Facial recognition", START_INSTRUCTIONS_CAMERA)
    build_instructions(250, START_Y_MIDDLE + 30, "Bluetooth retrieval:", START_INSTRUCTIONS_BLUETOOTH)

    pygame.display.flip()


def render_bluetooth_instructions(screen, devices, scroll_down_callback, confirm_callback, back_callback):
    selected = False
    scroll_index = 0
    last_scroll_index = -1

    print("[DISPLAY] Rendering Bluetooth instructions...")
    screen.fill(BACKGROUND_COLOR)

    title_text = TITLE_FONT.render("Discovered Bluetooth Devices", True, TITLE_COLOR)
    screen.blit(title_text, (SELECTED_DEV_X + 100, 30))

    y_offset = START_Y_TOP + 20
    for device in devices:
        device_text = f"Device {device.name} found with address: {device.address}"
        value_text = TEXT_FONT.render(device_text, True, TEXT_COLOR)
        screen.blit(value_text, (SELECTED_DEV_X, y_offset))
        y_offset += 25

    scroll_text = TEXT_FONT.render("Press the 2nd button from the left to scroll the list:", True, TITLE_COLOR)
    screen.blit(scroll_text, (SELECTED_DEV_X, SELECTED_DEV_Y - 20))

    currently_selected_text = TEXT_FONT.render(f"Selected device:   {devices[scroll_index].name}", True, TITLE_COLOR)
    screen.blit(currently_selected_text, (SELECTED_DEV_X, SELECTED_DEV_Y))
    pygame.display.flip()

    while not selected:
        scroll = scroll_down_callback()
        confirm = confirm_callback()
        back = back_callback()

        if back:
            selected = True
        
        if scroll:
            scroll_index = (scroll_index + 1) % len(devices)
            if scroll_index != last_scroll_index:
                pygame.draw.rect(screen, BACKGROUND_COLOR, pygame.Rect((SELECTED_DEV_X, SELECTED_DEV_Y, 400, 30)))
                selected_device = devices[scroll_index]
                currently_selected_text = TEXT_FONT.render(f"Selected device:   {selected_device.name}", True, TITLE_COLOR)
                screen.blit(currently_selected_text, (SELECTED_DEV_X, SELECTED_DEV_Y))
                last_scroll_index = scroll_index
                pygame.display.flip()

        if confirm:
            selected = True


def render_patient_data(screen, patient):
    print(f"[DISPLAY] Rendering patient data: {patient}")

    screen.fill(BACKGROUND_COLOR)
    pygame.draw.rect(screen, TITLE_COLOR, pygame.Rect(HEADER_BLOCK_DIM))

    def display_image():
        try:
            image_path = patient.get('image')
            patient_image = pygame.image.load(image_path)
            patient_image = pygame.transform.scale(patient_image, IMAGE_SIZE)
            screen.blit(patient_image, (IMAGE_X, IMAGE_Y))  

        except Exception as e:
            pygame.draw.rect(screen, (200, 200, 200), (IMAGE_X, IMAGE_Y, 180, 140))
            no_image_text = TEXT_FONT.render("No Image", True, TEXT_COLOR)
            screen.blit(no_image_text, (620, 110))

    def draw_card(title, items, start_x, start_y, width, height):
        pygame.draw.rect(screen, CARD_COLOR, (start_x, start_y, width, height))
        pygame.draw.rect(screen, BORDER_COLOR, (start_x, start_y, width, height), 1)
        title_text = TITLE_FONT.render(title, True, TITLE_COLOR)
        screen.blit(title_text, (start_x + 15, start_y + 15))

        y_offset = start_y + 50
        for item in items: 
            label = list(item.keys())[0]
            value = item[label]

            label_text = TEXT_FONT.render(label, False, TEXT_COLOR)
            value_text = TEXT_FONT.render(value, True, TEXT_COLOR)
            screen.blit(label_text, (start_x + 15, y_offset))
            screen.blit(value_text, (start_x + 160, y_offset))
            y_offset += 28

    # patient information
    name = {'Name': f"{patient.get('First Name', 'N/A')} {patient.get('Last Name', 'N/A')}"}
    date_of_birth = {'Date of Birth': patient.get('Date of Birth', 'N/A')}
    sex = {'Sex': patient.get('Gender', 'N/A')}
    conditions = [{'Condition': condition} for condition in patient['Conditions']] if patient['Conditions'] else [{'Condition': 'None'}]
    allergies = [{'Allergy': allergy} for allergy in patient['Allergies']] if patient['Allergies'] else [{'Allergy': 'None'}]
    medication = [{'Medicine': medicine} for medicine in patient['Medication']] if patient['Medication'] else [{'Medicine': 'None'}]

    display_image()
    draw_card("Information", [name, date_of_birth, sex], START_X_LEFT, START_Y_TOP, 500, 140)
    draw_card("Conditions", conditions, START_X_LEFT, START_Y_MIDDLE, CARD_WIDTH, CARD_HEIGHT)
    draw_card("Allergies", allergies, START_X_RIGHT, START_Y_MIDDLE, CARD_WIDTH, CARD_HEIGHT)
    draw_card("Medication", medication, START_X_LEFT, START_Y_BOTTOM, CARD_WIDTH, CARD_HEIGHT)
    draw_card("Emergency Contact", [], START_X_RIGHT, START_Y_BOTTOM, CARD_WIDTH, CARD_HEIGHT)

    pygame.display.flip()


def reset_display(screen):
    screen.fill((0, 0, 0))
    pygame.display.flip()
    return False
