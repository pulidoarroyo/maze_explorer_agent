import random

def generate_random_maze(grid, start, end):
    """Genera paredes aleatorias reiniciando el mapa primero"""
    for row in grid:
        for spot in row:
            spot.reset()
            # 30% de probabilidad de ser pared para asegurar que sea transitable frecuentemente
            if random.random() < 0.3 and spot != start and spot != end:
                spot.make_wall()
