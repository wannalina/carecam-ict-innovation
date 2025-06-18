import pygame

# define colors
BACKGROUND_COLOR = (245, 245, 245)
TEXT_COLOR = (30, 30, 30)
TITLE_COLOR = (0, 150, 230)
CARD_COLOR = (255, 255, 255)
BORDER_COLOR = (220, 220, 220)

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

def render_patient_data(screen, patient):
    print(f"[DISPLAY] Rendering patient data: {patient}")
    pygame.font.init()  # assicurati che il font system sia inizializzato
    title_font = pygame.font.Font(None, 30, bold=True)
    value_font = pygame.font.Font(None, 24, bold=True)    

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
            no_image_text = value_font.render("No Image", True, TEXT_COLOR)
            screen.blit(no_image_text, (620, 110))

    def draw_card(title, items, start_x, start_y, width, height):
        pygame.draw.rect(screen, CARD_COLOR, (start_x, start_y, width, height))
        pygame.draw.rect(screen, BORDER_COLOR, (start_x, start_y, width, height), 1)
        title_text = title_font.render(title, True, TITLE_COLOR)
        screen.blit(title_text, (start_x + 15, start_y + 15))

        y_offset = start_y + 50
        for item in items: 
            label = list(item.keys())[0]
            value = item[label]

            label_text = value_font.render(label, False, TEXT_COLOR)
            value_text = value_font.render(value, True, TEXT_COLOR)
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
