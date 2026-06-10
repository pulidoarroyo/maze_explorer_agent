import pygame
from src.config import get_config
from src.grid import make_grid
from src.maze_gen import generate_random_maze
from src.astar import algorithm
from src.renderer import draw

class AppState:
    def __init__(self, grid_width, window_width, window_height, ui_height):
        self.grid_width = grid_width
        self.window_width = window_width
        self.window_height = window_height
        self.ui_height = ui_height
        
    
        self.slider_val = 0.8
        self.slider_rect = pygame.Rect(0, 0, 180, 6)
        self.slider_handle_radius = 8
        self.dragging = False
        
        self.start_rect = pygame.Rect(0, 0, 130, 36)
        self.reset_rect = pygame.Rect(0, 0, 130, 36)
        
        self.is_running = False
        self.wants_reset = False
        self.path_found = None

    def get_delay(self):
        return int((1.0 - self.slider_val) * 200)

    def update_slider(self, mouse_x):
        x_min = self.slider_rect.x
        x_max = self.slider_rect.x + self.slider_rect.width
        mouse_x = max(x_min, min(mouse_x, x_max))
        self.slider_val = (mouse_x - x_min) / self.slider_rect.width

def run_algorithm(win, grid, start, end, app_state, rows, grid_width):
    app_state.is_running = True
    app_state.path_found = None
    for row in grid:
        for spot in row:
            if not spot.is_wall() and spot != start and spot != end:
                spot.reset()
    for row in grid:
        for spot in row:
            spot.update_neighbors(grid)
    draw_callback = lambda: draw(win, grid, rows, grid_width, app_state)
    found = algorithm(draw_callback, grid, start, end, app_state)
    app_state.is_running = False
    if app_state.wants_reset:
        app_state.wants_reset = False
       
        start, end = generate_random_maze(grid, start, end)
        app_state.path_found = None
        draw(win, grid, rows, grid_width, app_state)
    else:
        app_state.path_found = found
    return start, end

def main():
    pygame.init()
    
    # Obtener resolución de pantalla
    config = get_config()
    WIDTH = config["WIDTH"]
    HEIGHT = config["HEIGHT"]
    ROWS = config["ROWS"]
    GRID_SIZE = config["GRID_SIZE"]
    UI_HEIGHT = config["UI_HEIGHT"]
    CAPTION = config["CAPTION"]
    
    # Crear ventana 
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(CAPTION)
    
    # Crear cuadrícula
    grid = make_grid(ROWS, GRID_SIZE)
    
    start = grid[1][1]
    end = grid[ROWS - 2][ROWS - 2]
    start.make_start()
    end.make_end()
    
    start, end = generate_random_maze(grid, start, end)
    
    app_state = AppState(GRID_SIZE, WIDTH, HEIGHT, UI_HEIGHT)
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        draw(win, grid, ROWS, app_state.grid_width, app_state)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                
    
                slider_click_area = pygame.Rect(
                    app_state.slider_rect.x, app_state.slider_rect.y - 5,
                    app_state.slider_rect.width, app_state.slider_rect.height + 10
                )
                if slider_click_area.collidepoint(pos):
                    app_state.dragging = True
                    
                    app_state.update_slider(pos[0])
                elif app_state.start_rect.collidepoint(pos) and not app_state.is_running:
                    if not app_state.path_found:
                        app_state.path_found = None
                    start, end = run_algorithm(win, grid, start, end, app_state, ROWS, app_state.grid_width)
                elif app_state.reset_rect.collidepoint(pos) and not app_state.is_running:
                    app_state.wants_reset = False
                    start, end = generate_random_maze(grid, start, end)
                    app_state.path_found = None
                    draw(win, grid, ROWS, app_state.grid_width, app_state)
            
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                app_state.dragging = False
            
            if event.type == pygame.MOUSEMOTION and app_state.dragging:
                mouse_x, _ = pygame.mouse.get_pos()
                app_state.update_slider(mouse_x)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not app_state.is_running:
                    if not app_state.path_found:
                        app_state.path_found = None
                    start, end = run_algorithm(win, grid, start, end, app_state, ROWS, app_state.grid_width)
                if event.key == pygame.K_r and not app_state.is_running:
                    app_state.wants_reset = False
                    start, end = generate_random_maze(grid, start, end)
                    app_state.path_found = None
                    draw(win, grid, ROWS, app_state.grid_width, app_state)
        
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()