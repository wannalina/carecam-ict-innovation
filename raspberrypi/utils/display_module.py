import pygame

def render_patient_data(screen, patient):
    print(f"[DISPLAY] Rendering patient data: {patient}")
    pygame.font.init()  # assicurati che il font system sia inizializzato
    font = pygame.font.Font(None, 28)
    background_color = (255, 255, 255)
    text_color = (0, 0, 0)

    screen.fill(background_color)

    top_left = (20, 20)
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
    #render_block(["Conditions:"] + patient['Conditions'], top_right)
    render_block(["Allergies:"] + patient['Allergies'], bottom_left)
    render_block(["Medicines:"] + patient['Medication'], bottom_right)

    pygame.display.flip()
