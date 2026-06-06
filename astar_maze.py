import pygame
import math
import random
from queue import PriorityQueue

# Configuración de la ventana
WIDTH = 600
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Agente Explorador A*")

# Paleta de Colores
CLOSED_COLOR = (255, 99, 71)    # Rojo Tomate (Nodos explorados)
OPEN_COLOR = (144, 238, 144)    # Verde Claro (Nodos en frontera)
PATH_COLOR = (255, 215, 0)      # Dorado (Ruta óptima)
START_COLOR = (0, 191, 255)     # Azul (Inicio)
END_COLOR = (138, 43, 226)      # Violeta (Meta)
EMPTY_COLOR = (245, 245, 245)   # Blanco Humo (Camino libre)
WALL_COLOR = (47, 79, 79)       # Gris Oscuro (Obstáculos/Paredes)
GRID_COLOR = (200, 200, 200)    # Líneas de cuadrícula

class Nodo:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = EMPTY_COLOR
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_wall(self):
        return self.color == WALL_COLOR

    def reset(self):
        self.color = EMPTY_COLOR

    def make_start(self):
        self.color = START_COLOR

    def make_closed(self):
        self.color = CLOSED_COLOR

    def make_open(self):
        self.color = OPEN_COLOR

    def make_wall(self):
        self.color = WALL_COLOR

    def make_end(self):
        self.color = END_COLOR

    def make_path(self):
        self.color = PATH_COLOR

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        # Abajo
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_wall():
            self.neighbors.append(grid[self.row + 1][self.col])
        # Arriba
        if self.row > 0 and not grid[self.row - 1][self.col].is_wall():
            self.neighbors.append(grid[self.row - 1][self.col])
        # Derecha
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_wall():
            self.neighbors.append(grid[self.row][self.col + 1])
        # Izquierda
        if self.col > 0 and not grid[self.row][self.col - 1].is_wall():
            self.neighbors.append(grid[self.row][self.col - 1])

def h(p1, p2):
    """Heurística: Distancia de Manhattan"""
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
    """Pinta la ruta óptima encontrada al final"""
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def algorithm(draw, grid, start, end):
    """Implementación del Algoritmo A* (A-Star)"""
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    
    # g_score: costo desde el inicio hasta el nodo n
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    
    # f_score: g_score + heurística
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw() # Visualización en tiempo real de la exploración

        if current != start:
            current.make_closed()

    return False # No se encontró ruta

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Nodo(i, j, gap, rows)
            grid[i].append(spot)
    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GRID_COLOR, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GRID_COLOR, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
    win.fill(EMPTY_COLOR)
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()

def generate_random_maze(grid, start, end):
    """Genera paredes aleatorias reiniciando el mapa primero"""
    for row in grid:
        for spot in row:
            spot.reset()
            # 30% de probabilidad de ser pared para asegurar que sea transitable frecuentemente
            if random.random() < 0.3 and spot != start and spot != end:
                spot.make_wall()

def main(win, width):
    ROWS = 30
    grid = make_grid(ROWS, width)

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
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                # Iniciar el algoritmo con ESPACIO
                if event.key == pygame.K_SPACE:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                # Generar nuevo mapa y reiniciar con R
                if event.key == pygame.K_r:
                    generate_random_maze(grid, start, end)
                    start.make_start()
                    end.make_end()

    pygame.quit()

if __name__ == "__main__":
    main(WIN, WIDTH)