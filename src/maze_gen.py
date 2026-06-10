import random
from src.config import WALL_COLOR, START_COLOR, END_COLOR, EMPTY_COLOR

def generate_random_maze(grid, start, end, wall_prob=0.3):
    """Genera un laberinto aleatorio con inicio y fin en posiciones aleatorias."""
    rows = len(grid)
    
    # Limpia la cuadrícula 
    for i in range(rows):
        for j in range(rows):
            if grid[i][j] != start and grid[i][j] != end:
                if random.random() < wall_prob:
                    grid[i][j].make_wall()
                else:
                    grid[i][j].reset()
    
    all_positions = [(i, j) for i in range(rows) for j in range(rows)]
    random.shuffle(all_positions)
    
    # Buscar la posición para el inicio 
    start_found = False
    for i, j in all_positions:
        if not grid[i][j].is_wall():
            # Limpiar la posición anterior del start
            start.reset()
            # Actualizar 
            start = grid[i][j]
            start.make_start()
            start_found = True
            break
    
    # Buscar posición para la meta sin que coincida con una pared ni con el inicio
    end_found = False
    for i, j in all_positions:
        if not grid[i][j].is_wall() and grid[i][j] != start:
            end.reset()
            end = grid[i][j]
            end.make_end()
            end_found = True
            break
    
    # Usa esquinas de no encontrar posiciones válidas
    if not start_found:
        start.reset()
        start = grid[1][1]
        start.make_start()
    if not end_found:
        end.reset()
        end = grid[rows-2][rows-2]
        end.make_end()
    
    return start, end