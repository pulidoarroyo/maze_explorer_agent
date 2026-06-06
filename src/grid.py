from src.node import Nodo

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Nodo(i, j, gap, rows)
            grid[i].append(spot)
    return grid
