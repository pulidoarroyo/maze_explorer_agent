import pygame
from src.config import (
    EMPTY_COLOR, GRID_COLOR, UI_BG_COLOR, UI_TEXT_COLOR,
    SLIDER_TRACK_COLOR, SLIDER_HANDLE_COLOR, BUTTON_COLOR,
    BUTTON_HOVER_COLOR, BUTTON_ACTIVE_COLOR, BUTTON_TEXT_COLOR
)

# Cache de fuentes para evitar cargarlas repetidamente
_fonts = {}
def get_font(size, bold=False):
    key = (size, bold)
    if key not in _fonts:
        pygame.font.init()
        try:
            _fonts[key] = pygame.font.SysFont("Arial", size, bold=bold)
        except:
            _fonts[key] = pygame.font.SysFont(None, size, bold=bold)
    return _fonts[key]

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GRID_COLOR, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GRID_COLOR, (j * gap, 0), (j * gap, width))

def draw_ui(win, app_state):
    # Fondo del panel de control
    pygame.draw.rect(win, UI_BG_COLOR, (0, app_state.grid_width, app_state.grid_width, app_state.ui_height))
    # Línea separadora
    pygame.draw.line(win, (15, 23, 42), (0, app_state.grid_width), (app_state.grid_width, app_state.grid_width), 2)
    
    mouse_pos = pygame.mouse.get_pos()
    font_bold = get_font(14, True)
    font_normal = get_font(13, False)
    
    # --- SLIDER DE VELOCIDAD ---
    label_speed = font_bold.render("VELOCIDAD", True, UI_TEXT_COLOR)
    win.blit(label_speed, (20, app_state.grid_width + 15))
    
    # Dibujar pista del slider
    pygame.draw.rect(win, SLIDER_TRACK_COLOR, app_state.slider_rect, border_radius=4)
    
    # Posición de la manija
    handle_x = app_state.slider_rect.x + int(app_state.slider_val * app_state.slider_rect.width)
    handle_y = app_state.slider_rect.y + app_state.slider_rect.height // 2
    
    # Dibujar manija del slider (con borde blanco)
    pygame.draw.circle(win, (255, 255, 255), (handle_x, handle_y), app_state.slider_handle_radius)
    pygame.draw.circle(win, SLIDER_HANDLE_COLOR, (handle_x, handle_y), app_state.slider_handle_radius - 2)
    
    # Texto de retraso
    delay = app_state.get_delay()
    delay_text = f"Retraso: {delay} ms" if delay > 0 else "Sin retraso"
    txt_delay = font_normal.render(delay_text, True, UI_TEXT_COLOR)
    win.blit(txt_delay, (20, app_state.grid_width + 55))
    
    # --- BOTÓN INICIAR ---
    if app_state.is_running:
        start_btn_color = BUTTON_ACTIVE_COLOR
        start_text = "Buscando..."
    else:
        if app_state.start_rect.collidepoint(mouse_pos):
            start_btn_color = BUTTON_HOVER_COLOR
        else:
            start_btn_color = BUTTON_COLOR
        start_text = "Iniciar (Espacio)"
        
    pygame.draw.rect(win, start_btn_color, app_state.start_rect, border_radius=6)
    txt_start = font_bold.render(start_text, True, BUTTON_TEXT_COLOR)
    start_text_rect = txt_start.get_rect(center=app_state.start_rect.center)
    win.blit(txt_start, start_text_rect)
    
    # --- BOTÓN REINICIAR ---
    if app_state.reset_rect.collidepoint(mouse_pos):
        reset_btn_color = BUTTON_HOVER_COLOR
    else:
        reset_btn_color = BUTTON_COLOR
        
    pygame.draw.rect(win, reset_btn_color, app_state.reset_rect, border_radius=6)
    txt_reset = font_bold.render("Reiniciar (R)", True, BUTTON_TEXT_COLOR)
    reset_text_rect = txt_reset.get_rect(center=app_state.reset_rect.center)
    win.blit(txt_reset, reset_text_rect)
    
    # --- ESTADO DEL ALGORITMO ---
    status_text = "Listo"
    status_color = (203, 213, 225) # Slate 300
    if app_state.path_found is True:
        status_text = "¡Ruta encontrada!"
        status_color = (74, 222, 128) # Green 400
    elif app_state.path_found is False:
        status_text = "Sin ruta"
        status_color = (248, 113, 113) # Red 400
    elif app_state.is_running:
        status_text = "Buscando..."
        status_color = (96, 165, 250) # Blue 400
        
    lbl_status = font_bold.render("ESTADO:", True, UI_TEXT_COLOR)
    win.blit(lbl_status, (300, app_state.grid_width + 65))
    
    txt_status = font_bold.render(status_text, True, status_color)
    win.blit(txt_status, (365, app_state.grid_width + 65))

def draw(win, grid, rows, width, app_state=None):
    win.fill(EMPTY_COLOR)
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, width)
    if app_state is not None:
        draw_ui(win, app_state)
    pygame.display.update()

