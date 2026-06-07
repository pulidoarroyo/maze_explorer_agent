import pygame
from src.config import (
    EMPTY_COLOR, GRID_COLOR, UI_BG_COLOR, UI_TEXT_COLOR, UI_BORDER_COLOR,
    SLIDER_TRACK_COLOR, SLIDER_HANDLE_COLOR,
    BUTTON_COLOR, BUTTON_HOVER_COLOR, BUTTON_ACTIVE_COLOR, BUTTON_TEXT_COLOR,
    START_COLOR, END_COLOR, CLOSED_COLOR, OPEN_COLOR, PATH_COLOR
)

# ─── Fuentes del sistema ──────────────────────────────────────────────────────
_fonts = {}
def get_font(size, bold=False):
    key = (size, bold)
    if key not in _fonts:
        pygame.font.init()
        # Intentar fuentes sans-serif modernas
        for name in ["Segoe UI", "Arial", "Helvetica", "sans-serif", None]:
            try:
                _fonts[key] = pygame.font.SysFont(name, size, bold=bold)
                break
            except:
                continue
    return _fonts[key]

def _draw_pixel_border(win, rect, thickness=2):
    """Marco estilo RPG: borde doble con esquinas marcadas."""
    r = rect
    outer = pygame.Rect(r.x-thickness, r.y-thickness, r.width+thickness*2, r.height+thickness*2)
    pygame.draw.rect(win, (100, 70, 30), outer, thickness)          # borde exterior
    pygame.draw.rect(win, (60,  40, 15), r, thickness)              # borde interior
    # esquinas brillantes
    for cx, cy in [(outer.x, outer.y), (outer.right-1, outer.y),
                   (outer.x, outer.bottom-1), (outer.right-1, outer.bottom-1)]:
        pygame.draw.circle(win, (200, 150, 50), (cx, cy), thickness)

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GRID_COLOR, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GRID_COLOR, (j * gap, 0), (j * gap, width))

def draw_ui(win, app_state):
    gw = app_state.grid_width
    sw = app_state.sidebar_width

    # ── Fondo panel ──────────────────────────────────────────────────────────
    pygame.draw.rect(win, UI_BG_COLOR, (gw, 0, sw, gw))

    # Línea separadora pizarra (vertical)
    pygame.draw.line(win, UI_BORDER_COLOR, (gw, 0), (gw, gw), 1)

    mouse_pos = pygame.mouse.get_pos()
    font_sm   = get_font(12, False)
    font_md   = get_font(14, True)
    font_lg   = get_font(16, True)
    font_title = get_font(18, True)

    # ── TITULO ───────────────────────────────────────────────────────────────
    title_txt = font_title.render("Maze Explorer", True, UI_TEXT_COLOR)
    win.blit(title_txt, title_txt.get_rect(centerx=gw + sw // 2, y=20).topleft)
    
    subtitle_txt = font_sm.render("A* Dungeon Visualizer", True, (120, 130, 150))
    win.blit(subtitle_txt, subtitle_txt.get_rect(centerx=gw + sw // 2, y=42).topleft)

    # ── LEYENDA ───────────────────────────────────────────────────────────────
    legend = [
        (START_COLOR, "Inicio (Héroe)"),
        (END_COLOR, "Meta (Cofre)"),
        (CLOSED_COLOR, "Explorado"),
        (OPEN_COLOR, "Frontera"),
        (PATH_COLOR, "Ruta óptima"),
    ]
    ly = 85
    for color, label in legend:
        # Dibujar un bloque con esquinas ligeramente redondeadas
        pygame.draw.rect(win, color, (gw + 30, ly + 2, 12, 12), border_radius=2)
        pygame.draw.rect(win, UI_BORDER_COLOR, (gw + 30, ly + 2, 12, 12), 1, border_radius=2)
        win.blit(font_sm.render(label, True, (160, 175, 195)), (gw + 52, ly))
        ly += 25

    # ── SLIDER ───────────────────────────────────────────────────────────────
    lbl = font_sm.render("VELOCIDAD DE BÚSQUEDA", True, (160, 175, 195))
    win.blit(lbl, (gw + 20, 295))

    # Pista del slider con marco
    tr = app_state.slider_rect
    pygame.draw.rect(win, SLIDER_TRACK_COLOR, tr, border_radius=4)
    pygame.draw.rect(win, UI_BORDER_COLOR, tr, 1, border_radius=4)

    # Relleno proporcional
    fill_w = int(app_state.slider_val * tr.width)
    if fill_w > 2:
        pygame.draw.rect(win, SLIDER_HANDLE_COLOR, (tr.x, tr.y, fill_w, tr.height), border_radius=4)

    # Manija circular moderna (color blanco con borde índigo)
    hx = tr.x + fill_w
    hy = tr.y + tr.height // 2
    hr = app_state.slider_handle_radius
    pygame.draw.circle(win, (255, 255, 255), (hx, hy), hr)
    pygame.draw.circle(win, SLIDER_HANDLE_COLOR, (hx, hy), hr, 2)

    delay = app_state.get_delay()
    delay_txt = f"delay: {delay}ms" if delay > 0 else "velocidad: MAX"
    win.blit(font_sm.render(delay_txt, True, (120, 130, 150)), (gw + 20, 335))

    # ── BOTÓN INICIAR ─────────────────────────────────────────────────────────
    if app_state.is_running:
        if app_state.is_paused:
            bc = BUTTON_HOVER_COLOR if app_state.start_rect.collidepoint(mouse_pos) else BUTTON_COLOR
            bt = "> reanudar [SPC]"
        else:
            bc = BUTTON_ACTIVE_COLOR
            bt = "|| pausar [SPC]"
    elif app_state.start_rect.collidepoint(mouse_pos):
        bc = BUTTON_HOVER_COLOR
        bt = "> iniciar [SPC]"
    else:
        bc = BUTTON_COLOR
        bt = "> iniciar [SPC]"

    pygame.draw.rect(win, bc, app_state.start_rect, border_radius=6)
    pygame.draw.rect(win, UI_BORDER_COLOR, app_state.start_rect, 1, border_radius=6)
    win.blit(font_md.render(bt, True, BUTTON_TEXT_COLOR),
             font_md.render(bt, True, BUTTON_TEXT_COLOR).get_rect(center=app_state.start_rect.center).topleft)

    # ── BOTÓN REINICIAR ───────────────────────────────────────────────────────
    bc2 = BUTTON_HOVER_COLOR if app_state.reset_rect.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(win, bc2, app_state.reset_rect, border_radius=6)
    pygame.draw.rect(win, UI_BORDER_COLOR, app_state.reset_rect, 1, border_radius=6)
    rt = "> nuevo [R]"
    win.blit(font_md.render(rt, True, BUTTON_TEXT_COLOR),
             font_md.render(rt, True, BUTTON_TEXT_COLOR).get_rect(center=app_state.reset_rect.center).topleft)

    # ── ESTADO ────────────────────────────────────────────────────────────────
    if app_state.path_found is True:
        st, sc = "*** RUTA ENCONTRADA ***", (74, 222, 128)
    elif app_state.path_found is False:
        st, sc = "!!! SIN RUTA !!!", (248, 113, 113)
    elif app_state.is_running:
        st, sc = "... explorando ...", (96, 165, 250)
    else:
        st, sc = "[ listo ]", (156, 163, 175)

    status_surf = font_lg.render(st, True, sc)
    win.blit(status_surf, status_surf.get_rect(centerx=gw + sw // 2, y=545).topleft)


def draw(win, grid, rows, width, app_state=None):
    win.fill((18, 14, 10))
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, width)
    if app_state is not None:
        draw_ui(win, app_state)
    pygame.display.update()