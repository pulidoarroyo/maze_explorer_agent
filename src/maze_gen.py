import random

def generate_random_maze(grid, start, end):
    """
    Genera un laberinto perfecto usando DFS Recursive Backtracker.
    
    Un laberinto "perfecto" garantiza:
      - Exactamente UN camino entre cualquier par de celdas (árbol de expansión).
      - No hay islas aisladas: siempre existe solución entre start y end.
    
    Idea:
      La cuadrícula de ROWS×ROWS se trata como una grilla de celdas de tamaño 2×2
      (celdas "lógicas" en posiciones impares). Las paredes entre celdas lógicas
      ocupan las posiciones pares intermedias. El DFS "talla" el laberinto
      eliminando paredes entre celdas vecinas no visitadas.
    """
    rows = len(grid)

    # 1. Llenar todo de paredes
    for row in grid:
        for spot in row:
            spot.make_wall()

    # 2. Las celdas "lógicas" son las de índice impar en ambos ejes
    #    (1,1), (1,3), (3,1), (3,3), …
    def neighbors_logical(r, c):
        """Vecinos lógicos 2 pasos alejados (con pared intermedia)."""
        result = []
        for dr, dc in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            nr, nc = r + dr, c + dc
            if 1 <= nr < rows - 1 and 1 <= nc < rows - 1:
                result.append((nr, nc))
        return result

    # 3. DFS iterativo para tallar el laberinto
    start_r, start_c = 1, 1          # celda lógica inicial
    visited = set()
    visited.add((start_r, start_c))
    stack = [(start_r, start_c)]

    while stack:
        r, c = stack[-1]
        nbrs = [(nr, nc) for nr, nc in neighbors_logical(r, c)
                if (nr, nc) not in visited]

        if nbrs:
            nr, nc = random.choice(nbrs)
            # Abrir la pared intermedia entre (r,c) y (nr,nc)
            wall_r = (r + nr) // 2
            wall_c = (c + nc) // 2
            grid[wall_r][wall_c].reset()   # eliminar pared
            grid[nr][nc].reset()           # abrir celda destino
            grid[r][c].reset()             # asegurar celda actual abierta
            visited.add((nr, nc))
            stack.append((nr, nc))
        else:
            stack.pop()

    # 4. Restaurar start y end (pueden haber quedado sobreescritos)
    start.make_start()
    end.make_end()