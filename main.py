import pygame
from src.config import WIDTH, ROWS, CAPTION
from src.grid import make_grid
from src.maze_gen import generate_random_maze
from src.astar import algorithm
from src.renderer import draw

def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption(CAPTION)

    grid = make_grid(ROWS, WIDTH)

    # Definir inicio (arriba a la izquierda) y meta (abajo a la derecha) estáticos
    start = grid[1][1]
    end = grid[ROWS - 2][ROWS - 2]
    
    start.make_start()
    end.make_end()

    # Generar un laberinto inicial aleatorio
    generate_random_maze(grid, start, end)
    start.make_start()
    end.make_end()

    run = True
    while run:
        draw(win, grid, ROWS, WIDTH)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                # Iniciar el algoritmo con ESPACIO
                if event.key == pygame.K_SPACE:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    algorithm(lambda: draw(win, grid, ROWS, WIDTH), grid, start, end)

                # Generar nuevo mapa y reiniciar con R
                if event.key == pygame.K_r:
                    generate_random_maze(grid, start, end)
                    start.make_start()
                    end.make_end()

    pygame.quit()

if __name__ == "__main__":
    main()
