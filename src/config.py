import pygame

CLOSED_COLOR = (255, 99, 71)
OPEN_COLOR = (144, 238, 144)
PATH_COLOR = (255, 215, 0)
START_COLOR = (0, 191, 255)
END_COLOR = (138, 43, 226)
EMPTY_COLOR = (245, 245, 245)
WALL_COLOR = (47, 79, 79)
GRID_COLOR = (200, 200, 200)
UI_BG_COLOR = (30, 41, 59)
UI_TEXT_COLOR = (241, 245, 249)
SLIDER_TRACK_COLOR = (71, 85, 105)
SLIDER_HANDLE_COLOR = (59, 130, 246)
BUTTON_COLOR = (71, 85, 105)
BUTTON_HOVER_COLOR = (51, 65, 85)
BUTTON_ACTIVE_COLOR = (37, 99, 235)
BUTTON_TEXT_COLOR = (255, 255, 255)


TARGET_CELL_SIZE = 45          
UI_HEIGHT = 100                
MIN_ROWS = 10
MAX_ROWS = 50


def init_config():
    """Inicializa la configuración basada en la resolución de la pantalla."""
    pygame.display.init()  
    screen_info = pygame.display.Info()
    
   
    screen_width = screen_info.current_w
    screen_height = screen_info.current_h
    
    window_width = int(screen_width * 0.85)
    window_height = int(screen_height * 0.85)
    
    # Calcular el área disponible para la cuadrícula
    available_height = window_height - UI_HEIGHT
    max_grid_size = min(window_width, available_height)
    
    # Calcular número de filas segun el tamaño de las celdas
    rows = max(MIN_ROWS, min(MAX_ROWS, max_grid_size // TARGET_CELL_SIZE))
    cell_size = max_grid_size // rows
    grid_size = cell_size * rows
    
    # Ajustar ventana al tamaño exacto de la cuadrícula + UI
    final_width = grid_size
    final_height = grid_size + UI_HEIGHT
    
    return {
        "WIDTH": final_width,
        "HEIGHT": final_height,
        "UI_HEIGHT": UI_HEIGHT,
        "ROWS": rows,
        "CELL_SIZE": cell_size,
        "GRID_SIZE": grid_size,
        "CAPTION": "Agente Explorador A* con Control de Velocidad"
    }

# Configuración inicial 
CONFIG = None

def get_config():
    global CONFIG
    if CONFIG is None:
        CONFIG = init_config()
    return CONFIG