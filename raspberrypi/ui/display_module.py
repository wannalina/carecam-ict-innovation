import pygame

def render_patient_data(screen, patient):
    print(f"[DISPLAY] Rendering patient data: {patient}")
    pygame.font.init()  # assicurati che il font system sia inizializzato
    title_font = pygame.font.Font(None, 40)
    label_font = pygame.font.Font(None, 25)
    #font = pygame.font.Font(None, 28)

    # define colors
    BACKEGROUND_COLOR = (240, 248, 255)
    BLACK = (0, 0, 0)
    DARK_GRAY = (50, 50, 50)
    HEADER_BACKGROUND_COLOR = (220, 220, 220)

    screen.fill(BACKEGROUND_COLOR)

    '''top_left = (20, 20)
    top_right = (420, 20)
    bottom_left = (20, 260)
    bottom_right = (420, 260)

    def render_block(data_lines, start_pos):
        x, y = start_pos
        for line in data_lines:
            text_surface = font.render(line, True, text_color)
            screen.blit(text_surface, (x, y))
            y += 30

    general_info = [
        f"First Name: {patient.get('First Name', 'N/A')}",
        f"Last Name: {patient.get('Last Name', 'N/A')}",        
        f"Date of Birth: {patient.get('Date of Birth', 'N/A')}",
        f"Gender: {patient.get('Gender', 'N/A')}"
    ]

    render_block(general_info, top_left)
    render_block(["Conditions:"] + patient['Conditions'], top_right)
    render_block(["Allergies:"] + patient['Allergies'], bottom_left)
    render_block(["Medication:"] + patient['Medication'], bottom_right)'''
    
    def draw_section(title, items, start_x, start_y):
        header_rect = pygame.Rect(start_x, start_y, 360, 35)
        pygame.draw.rect(screen, HEADER_BACKGROUND_COLOR, header_rect)
        header_text = title_font.render(title, True, DARK_GRAY)
        screen.blit(header_text, (start_x + 10, start_y + 5))
        
        y_offset = start_y + 45
        for item in items: 
            line = label_font.render(f"¤ {item}", True, BLACK)
            screen.blit(line, (start_x + 50, y_offset))
            y_offset += 28
    
    name = f"{patient.get('First Name', 'N/A')} {patient.get('Last Name')}"
    date_of_birth = f"{patient.get('Date of Birth', 'N/A')}"
    sex = f"{patient.get('Gender', 'N/A')}"
    
    draw_section("Patient Information", [f"Name: {name}", f"Date of Birth: {date_of_birth}", f"Sex: {sex}"], 20, 20)
    draw_section("Conditions", patient['Conditions'], 420, 20)
    draw_section("Allergies", patient['Allergies'], 20, 250)
    draw_section("Medications", patient['Medication'], 420, 250)

    pygame.display.flip()
