import pygame
from src.config import (
    EMPTY_COLOR, GRID_COLOR, UI_BG_COLOR, UI_TEXT_COLOR,
    SLIDER_TRACK_COLOR, SLIDER_HANDLE_COLOR, BUTTON_COLOR,
    BUTTON_HOVER_COLOR, BUTTON_ACTIVE_COLOR, BUTTON_TEXT_COLOR
)

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

def draw_grid(win, rows, grid_width):
    gap = grid_width // rows
    for i in range(rows):
        pygame.draw.line(win, GRID_COLOR, (0, i * gap), (grid_width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GRID_COLOR, (j * gap, 0), (j * gap, grid_width))

def get_status_info(app_state):
    #Lógica del estado
    if app_state.is_running:
        return {"text": "Buscando...", "color": (96, 165, 250)}
    elif app_state.path_found is True:
        return {"text": "¡Ruta encontrada!", "color": (74, 222, 128)}
    elif app_state.path_found is False:
        return {"text": "Sin ruta", "color": (248, 113, 113)}
    else:
        return {"text": "Listo", "color": (203, 213, 225)}

def draw_ui(win, app_state, grid_width, ui_height, rows):
    y_base = grid_width
    
    # Fondo del panel
    pygame.draw.rect(win, UI_BG_COLOR, (0, y_base, grid_width, ui_height))
    pygame.draw.line(win, (15, 23, 42), (0, y_base), (grid_width, y_base), 3)
    
    mouse_pos = pygame.mouse.get_pos()
    font_bold = get_font(14, True)
    font_normal = get_font(13, False)
    
   
    label_speed = font_bold.render("VELOCIDAD", True, UI_TEXT_COLOR)
    win.blit(label_speed, (20, y_base + 12))
    
    app_state.slider_rect = pygame.Rect(130, y_base + 16, 180, 6)
    pygame.draw.rect(win, SLIDER_TRACK_COLOR, app_state.slider_rect, border_radius=3)
    
    handle_x = app_state.slider_rect.x + int(app_state.slider_val * app_state.slider_rect.width)
    handle_y = app_state.slider_rect.y + app_state.slider_rect.height // 2
    pygame.draw.circle(win, (255, 255, 255), (handle_x, handle_y), app_state.slider_handle_radius)
    pygame.draw.circle(win, SLIDER_HANDLE_COLOR, (handle_x, handle_y), app_state.slider_handle_radius - 2)
    
    delay = app_state.get_delay()
    delay_text = f"Retraso: {delay} ms" if delay > 0 else "Sin retraso"
    txt_delay = font_normal.render(delay_text, True, UI_TEXT_COLOR)
    win.blit(txt_delay, (330, y_base + 12))
    
    button_y = y_base + 45
    status_y = y_base + 45
    
    status = get_status_info(app_state)
    lbl_status = font_bold.render("ESTADO:", True, UI_TEXT_COLOR)
    win.blit(lbl_status, (20, status_y))
    
    txt_status = font_bold.render(status["text"], True, status["color"])
    win.blit(txt_status, (100, status_y))
    
    button_w = 110
    button_h = 32
    spacing = 20
    total_w = 2 * button_w + spacing
  
    start_x = grid_width - total_w - 20
    
    app_state.start_rect = pygame.Rect(start_x, button_y, button_w, button_h)
    app_state.reset_rect = pygame.Rect(start_x + button_w + spacing, button_y, button_w, button_h)
    
    # Botón Iniciar
    if app_state.is_running:
        btn_color = BUTTON_ACTIVE_COLOR
        btn_text = "DETENER"
    else:
        btn_color = BUTTON_HOVER_COLOR if app_state.start_rect.collidepoint(mouse_pos) else BUTTON_COLOR
        btn_text = "INICIAR"
    
    pygame.draw.rect(win, btn_color, app_state.start_rect, border_radius=8)
    txt_start = font_bold.render(btn_text, True, BUTTON_TEXT_COLOR)
    win.blit(txt_start, txt_start.get_rect(center=app_state.start_rect.center))
    
    # Botón Reiniciar
    btn_color = BUTTON_HOVER_COLOR if app_state.reset_rect.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(win, btn_color, app_state.reset_rect, border_radius=8)
    txt_reset = font_bold.render("REINICIAR", True, BUTTON_TEXT_COLOR)
    win.blit(txt_reset, txt_reset.get_rect(center=app_state.reset_rect.center))

def draw(win, grid, rows, grid_width, app_state):
    win.fill(EMPTY_COLOR)
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, grid_width)
    draw_ui(win, app_state, grid_width, app_state.ui_height, rows)
    pygame.display.update()