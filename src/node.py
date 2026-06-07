import pygame
from src.config import (
    CLOSED_COLOR, OPEN_COLOR, PATH_COLOR, START_COLOR,
    END_COLOR, EMPTY_COLOR, WALL_COLOR, GRID_COLOR
)

# ─── Colores internos para identificar el tipo de nodo ───────────────────────
_WALL_TAG   = (1, 1, 1)   # tag único, no se dibuja directamente

class Nodo:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x   = col * width     # x = columna → posición horizontal
        self.y   = row * width     # y = fila    → posición vertical
        self.color = EMPTY_COLOR
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):     return self.row, self.col
    def is_wall(self):     return self.color == _WALL_TAG
    def reset(self):       self.color = EMPTY_COLOR
    def make_start(self):  self.color = START_COLOR
    def make_closed(self): self.color = CLOSED_COLOR
    def make_open(self):   self.color = OPEN_COLOR
    def make_wall(self):   self.color = _WALL_TAG
    def make_end(self):    self.color = END_COLOR
    def make_path(self):   self.color = PATH_COLOR

    # ── Helpers de dibujo pixel-art ──────────────────────────────────────────

    def _draw_floor(self, win, x, y, w):
        """Suelo de dungeon oscuro con variación sutil por posición."""
        base = (18, 14, 10)
        # Pequeña variación estática basada en posición para textura
        v = ((self.row * 7 + self.col * 13) % 5)
        c = (base[0]+v, base[1]+v, base[2]+v)
        pygame.draw.rect(win, c, (x, y, w, w))

    def _draw_wall(self, win, x, y, w):
        """Bloque de piedra con borde iluminado arriba/izquierda y sombra abajo/derecha."""
        # Cuerpo
        pygame.draw.rect(win, (55, 42, 28), (x, y, w, w))
        # Línea de grieta horizontal a la mitad
        mid = y + w // 2
        pygame.draw.line(win, (35, 27, 18), (x+1, mid), (x+w-2, mid), 1)
        # Grieta vertical (offset según par/impar)
        off = (w // 4) if (self.row + self.col) % 2 == 0 else (3 * w // 4)
        pygame.draw.line(win, (35, 27, 18), (x+off, y+1), (x+off, mid-1), 1)
        off2 = w - off
        pygame.draw.line(win, (35, 27, 18), (x+off2, mid+1), (x+off2, y+w-2), 1)
        # Highlight superior
        pygame.draw.line(win, (90, 72, 48), (x, y), (x+w-1, y), 1)
        pygame.draw.line(win, (90, 72, 48), (x, y), (x, y+w-1), 1)
        # Sombra inferior
        pygame.draw.line(win, (25, 18, 10), (x, y+w-1), (x+w-1, y+w-1), 1)
        pygame.draw.line(win, (25, 18, 10), (x+w-1, y), (x+w-1, y+w-1), 1)

    def _draw_explored(self, win, x, y, w):
        """Suelo con mancha azul tenue — nodo visitado."""
        self._draw_floor(win, x, y, w)
        s = pygame.Surface((w, w), pygame.SRCALPHA)
        s.fill((20, 60, 110, 120))
        win.blit(s, (x, y))

    def _draw_frontier(self, win, x, y, w):
        """Suelo con brillo verde — nodo en frontera."""
        self._draw_floor(win, x, y, w)
        s = pygame.Surface((w, w), pygame.SRCALPHA)
        s.fill((60, 160, 50, 140))
        win.blit(s, (x, y))
        # puntito central brillante
        cx, cy = x + w//2, y + w//2
        r = max(2, w//5)
        pygame.draw.circle(win, (140, 255, 100, 200), (cx, cy), r)

    def _draw_path(self, win, x, y, w):
        """Suelo con gema dorada centrada — ruta óptima."""
        self._draw_floor(win, x, y, w)
        s = pygame.Surface((w, w), pygame.SRCALPHA)
        s.fill((200, 160, 0, 80))
        win.blit(s, (x, y))
        cx, cy = x + w//2, y + w//2
        r = max(2, w//4)
        pygame.draw.circle(win, (255, 210, 30), (cx, cy), r)
        pygame.draw.circle(win, (255, 255, 180), (cx - r//3, cy - r//3), max(1, r//3))

    def _draw_start(self, win, x, y, w):
        """Hero pixel — triángulo verde con ojos."""
        self._draw_floor(win, x, y, w)
        cx, cy = x + w//2, y + w//2
        body_r = max(3, w//3)
        # Cuerpo
        pygame.draw.circle(win, (50, 200, 80), (cx, cy), body_r)
        # Brillo
        pygame.draw.circle(win, (140, 255, 160), (cx - body_r//3, cy - body_r//3), max(1, body_r//3))
        # Borde
        pygame.draw.circle(win, (20, 120, 40), (cx, cy), body_r, 1)

    def _draw_end(self, win, x, y, w):
        """Cofre dorado — rectángulo con tapa y brillo."""
        self._draw_floor(win, x, y, w)
        p = max(2, w // 5)
        bw, bh = w - p*2, w - p*2
        bx, by = x + p, y + p
        # Cuerpo del cofre
        pygame.draw.rect(win, (160, 100, 20), (bx, by + bh//3, bw, bh*2//3))
        # Tapa
        pygame.draw.rect(win, (200, 140, 30), (bx, by, bw, bh//3 + 1))
        # Cerradura
        lx = bx + bw//2 - 1
        ly = by + bh//3
        pygame.draw.rect(win, (255, 220, 60), (lx, ly, 3, 3))
        # Brillo
        pygame.draw.line(win, (255, 240, 120), (bx+2, by+2), (bx+bw//3, by+2), 1)

    def draw(self, win):
        x, y, w = self.x, self.y, self.width

        if self.color == _WALL_TAG:
            self._draw_wall(win, x, y, w)
        elif self.color == EMPTY_COLOR:
            self._draw_floor(win, x, y, w)
        elif self.color == CLOSED_COLOR:
            self._draw_explored(win, x, y, w)
        elif self.color == OPEN_COLOR:
            self._draw_frontier(win, x, y, w)
        elif self.color == PATH_COLOR:
            self._draw_path(win, x, y, w)
        elif self.color == START_COLOR:
            self._draw_start(win, x, y, w)
        elif self.color == END_COLOR:
            self._draw_end(win, x, y, w)
        else:
            pygame.draw.rect(win, self.color, (x, y, w, w))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_wall():
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_wall():
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_wall():
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_wall():
            self.neighbors.append(grid[self.row][self.col - 1])