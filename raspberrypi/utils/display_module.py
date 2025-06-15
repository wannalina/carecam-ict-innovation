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
        f"Name: {patient.get('name', 'N/A')}",
        f"Age: {patient.get('age', 'N/A')}",
        f"Blood type: {patient.get('blood_type', 'N/A')}"
    ]

    render_block(general_info, top_left)
    render_block(["Conditions:"] + patient['conditions'], top_right)
    render_block(["Allergies:"] + patient['allergies'], bottom_left)
    render_block(["Medicines:"] + patient['medicines'], bottom_right)

    pygame.display.flip()
