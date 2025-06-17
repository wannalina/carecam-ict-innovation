import pygame

def render_patient_data(screen, patient):
    print(f"[DISPLAY] Rendering patient data: {patient}")
    pygame.font.init()  # assicurati che il font system sia inizializzato
    title_font = pygame.font.Font(None, 40)
    label_font = pygame.font.Font(None, 25)

    # define colors
    BACKEGROUND_COLOR = (240, 248, 255)
    BLACK = (0, 0, 0)
    DARK_GRAY = (50, 50, 50)
    HEADER_BACKGROUND_COLOR = (220, 220, 220)

    screen.fill(BACKEGROUND_COLOR)

    def display_image():
        try:
            image_path = patient.get('image')
            patient_image = pygame.image.load(image_path)
            patient_image = pygame.transform.scale(patient_image, (140, 140))
            screen.blit(patient_image, (640, 20))  # moved image to top-right corner
        except Exception as e:
            pygame.draw.rect(screen, (200, 200, 200), (640, 20, 140, 140))
            no_image_text = label_font.render("No Image", True, DARK_GRAY)
            screen.blit(no_image_text, (660, 80))

    def draw_section(title, items, start_x, start_y, width=360):
        header_rect = pygame.Rect(start_x, start_y, width, 35)
        pygame.draw.rect(screen, HEADER_BACKGROUND_COLOR, header_rect)
        header_text = title_font.render(title, True, DARK_GRAY)
        screen.blit(header_text, (start_x + 10, start_y + 5))

        y_offset = start_y + 45
        for item in items: 
            line = label_font.render(f"• {item}", True, BLACK)
            screen.blit(line, (start_x + 20, y_offset))
            y_offset += 28

    name = f"{patient.get('First Name', 'N/A')} {patient.get('Last Name')}"
    date_of_birth = f"{patient.get('Date of Birth', 'N/A')}"
    sex = f"{patient.get('Gender', 'N/A')}"

    display_image()
    draw_section("Patient Information", [f"Name: {name}", f"Date of Birth: {date_of_birth}", f"Sex: {sex}"], 20, 20)
    draw_section("Conditions", patient['Conditions'], 20, 200)
    draw_section("Allergies", patient['Allergies'], 420, 200)
    draw_section("Medications", patient['Medication'], 20, 380)

    pygame.display.flip()
