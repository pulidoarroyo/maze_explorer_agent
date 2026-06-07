import pygame

# ─── Paleta pixel-art / dungeon ───────────────────────────────────────────────
WALL_COLOR      = (40,  30,  20)   # base de bloque (no se usa directamente)
EMPTY_COLOR     = (18,  14,  10)   # suelo del dungeon
GRID_COLOR      = (30,  24,  16)   # líneas de cuadrícula (casi invisibles)

CLOSED_COLOR    = (30,  60,  90)   # nodos explorados: azul dungeon
OPEN_COLOR      = (80, 160,  60)   # frontera: verde mágico
PATH_COLOR      = (255, 200,   0)  # ruta: dorado brillante
START_COLOR     = (50, 200,  80)   # inicio (verde héroe)
END_COLOR       = (220, 160,   0)  # meta (dorado cofre)

# UI - Estilo moderno oscuro / minimalista
UI_BG_COLOR          = (18,  24,  38)    # Gris azulado muy oscuro y elegante
UI_TEXT_COLOR        = (243, 244, 246)   # Blanco roto para alta legibilidad
UI_BORDER_COLOR      = (45,  55,  72)    # Gris pizarra suave
SLIDER_TRACK_COLOR   = (30,  41,  59)    # Fondo del slider
SLIDER_HANDLE_COLOR  = (99,  102, 241)   # Índigo vibrante moderno
BUTTON_COLOR         = (31,  41,  55)    # Botón base
BUTTON_HOVER_COLOR   = (55,  65,  81)    # Botón hover
BUTTON_ACTIVE_COLOR  = (79,  70,  229)   # Índigo activo (buscando/pausado)
BUTTON_TEXT_COLOR    = (255, 255, 255)   # Texto de botón blanco puro

# ─── Dimensiones ──────────────────────────────────────────────────────────────
GRID_WIDTH     = 600
SIDEBAR_WIDTH  = 250
WIDTH          = GRID_WIDTH + SIDEBAR_WIDTH
HEIGHT         = GRID_WIDTH
ROWS           = 30
CAPTION        = "Maze Explorer"