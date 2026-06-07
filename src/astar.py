import pygame
import sys
from queue import PriorityQueue

def h(p1, p2):
    """Heurística: Distancia de Manhattan"""
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw, app_state):
    """Pinta la ruta óptima encontrada al final"""
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()
        # Aplicar retardo también al pintar la ruta
        if app_state.get_delay() > 0:
            pygame.time.delay(app_state.get_delay())

def algorithm(draw, grid, start, end, app_state):
    """Implementación del Algoritmo A* (A-Star) con control de velocidad en tiempo real"""
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
        # Procesar eventos de la UI durante la ejecución del algoritmo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Click izquierdo
                    pos = pygame.mouse.get_pos()
                    # Verificar si se hizo click en el slider para arrastrarlo
                    slider_click_area = pygame.Rect(
                        app_state.slider_rect.x,
                        app_state.slider_rect.y - 5,
                        app_state.slider_rect.width,
                        app_state.slider_rect.height + 10
                    )
                    if slider_click_area.collidepoint(pos):
                        app_state.dragging = True
                    # Permitir reiniciar (cancelar) a la mitad de la búsqueda
                    elif app_state.reset_rect.collidepoint(pos):
                        app_state.is_running = False
                        app_state.wants_reset = True
                        return False

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    app_state.dragging = False

            if event.type == pygame.MOUSEMOTION:
                if app_state.dragging:
                    mouse_x, _ = pygame.mouse.get_pos()
                    app_state.update_slider(mouse_x)

            if event.type == pygame.KEYDOWN:
                # Permitir cancelar con la tecla R
                if event.key == pygame.K_r:
                    app_state.is_running = False
                    app_state.wants_reset = True
                    return False

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw, app_state)
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
                    
                    # CORRECCIÓN: Solo se hace verde si NO es la meta
                    if neighbor != end:
                        neighbor.make_open()

        draw() # Visualización en tiempo real de la exploración

        if current != start:
            current.make_closed()

        # Aplicar el retardo de visualización dinámico
        if app_state.get_delay() > 0:
            pygame.time.delay(app_state.get_delay())

    return False # No se encontró ruta