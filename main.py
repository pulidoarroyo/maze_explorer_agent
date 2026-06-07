import pygame
from src.config import WIDTH, HEIGHT, GRID_WIDTH, SIDEBAR_WIDTH, ROWS, CAPTION
from src.grid import make_grid
from src.maze_gen import generate_random_maze
from src.astar import algorithm
from src.renderer import draw

class AppState:
    def __init__(self, grid_width, sidebar_width):
        self.grid_width = grid_width
        self.sidebar_width = sidebar_width
        
        # Posicionamiento del slider en la barra lateral
        slider_x = grid_width + 20
        self.slider_rect = pygame.Rect(slider_x, 320, 210, 8)
        self.slider_handle_radius = 8
        self.slider_val = 0.8  # Valor entre 0.0 y 1.0 (80% velocidad por defecto)
        self.dragging = False
        
        # Posicionamiento de botones en la barra lateral
        self.start_rect = pygame.Rect(slider_x, 420, 210, 40)
        self.reset_rect = pygame.Rect(slider_x, 480, 210, 40)
        
        self.is_running = False
        self.is_paused = False
        self.wants_reset = False
        self.path_found = None

    def get_delay(self):
        # 1.0 velocidad -> 0ms retraso
        # 0.0 velocidad -> 200ms retraso
        return int((1.0 - self.slider_val) * 200)

    def update_slider(self, mouse_x):
        x_min = self.slider_rect.x
        x_max = self.slider_rect.x + self.slider_rect.width
        mouse_x = max(x_min, min(mouse_x, x_max))
        self.slider_val = (mouse_x - x_min) / self.slider_rect.width

def run_algorithm(win, grid, start, end, app_state):
    app_state.is_running = True
    app_state.path_found = None
    
    # Limpiar caminos previos antes de comenzar una nueva búsqueda, conservando las paredes
    for row in grid:
        for spot in row:
            if not spot.is_wall() and spot != start and spot != end:
                spot.reset()
                
    for row in grid:
        for spot in row:
            spot.update_neighbors(grid)
            
    # Ejecutar algoritmo (pasando GRID_WIDTH en lugar de WIDTH)
    found = algorithm(lambda: draw(win, grid, ROWS, GRID_WIDTH, app_state), grid, start, end, app_state)
    
    app_state.is_running = False
    if app_state.wants_reset:
        app_state.wants_reset = False
        generate_random_maze(grid, start, end)
        start.make_start()
        end.make_end()
        app_state.path_found = None
    else:
        app_state.path_found = found

def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(CAPTION)

    grid = make_grid(ROWS, GRID_WIDTH)
    app_state = AppState(GRID_WIDTH, SIDEBAR_WIDTH)

    # Definir inicio (arriba a la izquierda) y meta (abajo a la derecha) estáticos
    start = grid[1][1]
    end = grid[ROWS - 3][ROWS - 3]
    
    start.make_start()
    end.make_end()

    # Generar un laberinto inicial aleatorio
    generate_random_maze(grid, start, end)
    start.make_start()
    end.make_end()

    run = True
    while run:
        draw(win, grid, ROWS, GRID_WIDTH, app_state)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    slider_click_area = pygame.Rect(
                        app_state.slider_rect.x,
                        app_state.slider_rect.y - 5,
                        app_state.slider_rect.width,
                        app_state.slider_rect.height + 10
                    )
                    if slider_click_area.collidepoint(pos):
                        app_state.dragging = True
                    elif app_state.start_rect.collidepoint(pos) and not app_state.is_running:
                        run_algorithm(win, grid, start, end, app_state)
                    elif app_state.reset_rect.collidepoint(pos):
                        generate_random_maze(grid, start, end)
                        start.make_start()
                        end.make_end()
                        app_state.path_found = None

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    app_state.dragging = False

            if event.type == pygame.MOUSEMOTION:
                if app_state.dragging:
                    mouse_x, _ = pygame.mouse.get_pos()
                    app_state.update_slider(mouse_x)

            if event.type == pygame.KEYDOWN:
                # Iniciar el algoritmo con ESPACIO
                if event.key == pygame.K_SPACE and not app_state.is_running:
                    run_algorithm(win, grid, start, end, app_state)

                # Generar nuevo mapa y reiniciar con R
                if event.key == pygame.K_r:
                    generate_random_maze(grid, start, end)
                    start.make_start()
                    end.make_end()
                    app_state.path_found = None

    pygame.quit()

if __name__ == "__main__":
    main()