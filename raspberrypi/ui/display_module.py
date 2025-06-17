import pygame

def render_patient_data(screen, patient):
    print(f"[DISPLAY] Rendering patient data: {patient}")
    pygame.font.init()  # assicurati che il font system sia inizializzato
    title_font = pygame.font.Font(None, 28, bold=True)
    value_font = pygame.font.Font(None, 22, bold=True)

    # define colors
    BACKGROUND_COLOR = (245, 245, 245)
    TEXT_COLOR = (30, 30, 30)
    TITLE_COLOR = (0, 150, 230)
    CARD_COLOR = (255, 255, 255)
    BORDER_COLOR = (220, 220, 220)

    IMAGE_SIZE = (180, 160)
    IMAGE_X = 560
    IMAGE_Y = 20

    screen.fill(BACKGROUND_COLOR)

    def display_image():
        try:
            image_path = patient.get('image')
            patient_image = pygame.image.load(image_path)
            patient_image = pygame.transform.scale(patient_image, IMAGE_SIZE)
            screen.blit(patient_image, (IMAGE_X, IMAGE_Y))  # moved image to top-right corner
        except Exception as e:
            pygame.draw.rect(screen, (200, 200, 200), (IMAGE_X, IMAGE_Y, IMAGE_SIZE))
            no_image_text = label_font.render("No Image", True, TEXT_COLOR)
            screen.blit(no_image_text, (660, 80))

    def draw_card(title, items, start_x, start_y, width=360, height=100):
        pygame.draw.rect(screen, CARD_COLOR, (start_x, start_y, width, height))
        pygame.draw.rect(screen, BORDER_COLOR, (start_x, start_y, width, height), 1)
        title_text = title_font.render(title, True, TITLE_COLOR)
        screen.blit(title_text, (start_x + 10, start_y + 5))

        y_offset = start_y + 40
        for item in items: 
            value_text = value_font.render(item, True, TEXT_COLOR)
            screen.blit(value_text, (start_x + 140, y_offset))
            y_offset += 28

    # patient information
    name = f"{patient.get('First Name', 'N/A')} {patient.get('Last Name')}"
    date_of_birth = f"{patient.get('Date of Birth', 'N/A')}"
    sex = f"{patient.get('Gender', 'N/A')}"

    display_image()
    draw_card("Information", [name, date_of_birth, sex], 20, 20, 500, 160)
    draw_card("Conditions", patient["Conditions"], 20, 200, 360, 100)
    draw_card("Allergies", patient["Allergies"], 420, 200, 360, 100)
    draw_card("Medication", patient["Medication"], 20, 320, 360, 100)
    '''draw_section("Patient Information", [f"Name: {name}", f"Date of Birth: {date_of_birth}", f"Sex: {sex}"], 20, 20)
    draw_section("Conditions", patient['Conditions'], 20, 200)
    draw_section("Allergies", patient['Allergies'], 420, 200)
    draw_section("Medications", patient['Medication'], 20, 380)'''

    pygame.display.flip()
