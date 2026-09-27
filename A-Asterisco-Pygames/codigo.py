import pygame
import heapq
import random
import sys

# ---------------- Configuración ----------------
ROWS, COLS = 20, 20
CELL = 30
HEADER = 50
WIDTH = COLS * CELL
HEIGHT = ROWS * CELL + HEADER
FPS = 60

# ---------------- Colores ----------------
C_BG      = (24, 26, 32)
C_GRID    = (60, 64, 76)
C_EMPTY   = (240, 240, 245)
C_WALL    = (45, 48, 56)
C_START   = (46, 204, 113)
C_GOAL    = (231, 76, 60)
C_OPEN    = (255, 176, 59)    # frontera (en el heap, sin expandir)
C_CLOSED  = (116, 185, 255)   # ya expandidos
C_CURRENT = (255, 105, 180)   # nodo que se acaba de expandir
C_PATH    = (255, 224, 102)   # camino final
C_TEXT    = (230, 230, 230)


# ---------------- A* instrumentado ----------------
class AStarVisualizer:
    """A* que expone su estado interno para poder dibujarlo paso a paso."""

    def __init__(self, walls, start, goal):
        self.walls = walls
        self.start = start
        self.goal = goal
        self.reset()

    def reset(self):
        self.open_heap = []
        self.g_score = {self.start: 0}
        self.came_from = {}
        self.closed = set()
        self.current = None
        self.path = None
        self.finished = False
        self.no_path = False
        heapq.heappush(
            self.open_heap, (self._h(self.start), 0, self.start)
        )

    def _h(self, a):
        return abs(a[0] - self.goal[0]) + abs(a[1] - self.goal[1])

    def _neighbors(self, pos):
        r, c = pos
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if (0 <= nr < ROWS and 0 <= nc < COLS
                    and (nr, nc) not in self.walls):
                yield (nr, nc)

    def step(self):
        """Expande exactamente un nodo (o termina)."""
        if self.finished:
            return

        # Saltamos entradas obsoletas del heap
        while self.open_heap:
            f, g, current = heapq.heappop(self.open_heap)
            if current in self.closed:
                continue

            self.closed.add(current)
            self.current = current

            # ¿Es la meta?
            if current == self.goal:
                path = [current]
                node = current
                while node in self.came_from:
                    node = self.came_from[node]
                    path.append(node)
                path.reverse()
                self.path = path
                self.finished = True
                return

            # Expandimos vecinos
            for nxt in self._neighbors(current):
                new_g = self.g_score[current] + 1
                if nxt not in self.g_score or new_g < self.g_score[nxt]:
                    self.g_score[nxt] = new_g
                    self.came_from[nxt] = current
                    heapq.heappush(
                        self.open_heap,
                        (new_g + self._h(nxt), new_g, nxt)
                    )
            return  # una expansión por llamada

        # Heap vacío => no hay camino
        self.no_path = True
        self.finished = True


# ---------------- Helpers de dibujo ----------------
def cell_rect(r, c):
    return pygame.Rect(c * CELL, HEADER + r * CELL, CELL, CELL)


def mouse_to_cell(pos):
    x, y = pos
    if y < HEADER:
        return None
    r = (y - HEADER) // CELL
    c = x // CELL
    if 0 <= r < ROWS and 0 <= c < COLS:
        return (r, c)
    return None


def draw_header(screen, font, algo, running, speed):
    pygame.draw.rect(screen, C_BG, (0, 0, WIDTH, HEADER))
    if algo is None:
        status = "-"
    elif algo.finished:
        status = "SIN CAMINO" if algo.no_path else "CAMINO ENCONTRADO"
    elif running:
        status = "BUSCANDO..."
    else:
        status = "PAUSA"
    line1 = (f"ESPACIO:play/pause   S:paso   R:reset   C:limpiar   "
             f"M:maze   +/-:vel  ({speed}/s)")
    line2 = f"Estado: {status}   (arrastra inicio/meta, click=dibujar, "
    line3 = "  click-dcho=borrar)"
    screen.blit(font.render(line1, True, C_TEXT), (8, 4))
    screen.blit(font.render(line2 + line3, True, C_TEXT), (8, 24))


def draw_scene(screen, font, algo, walls, start, goal, running, speed):
    screen.fill(C_BG)
    draw_header(screen, font, algo, running, speed)

    # Celdas vacías
    for r in range(ROWS):
        for c in range(COLS):
            pygame.draw.rect(screen, C_EMPTY, cell_rect(r, c))

    # Estado del algoritmo
    if algo is not None:
        open_set = set(algo.g_score.keys()) - algo.closed
        for cell in open_set:
            if cell in (start, goal):
                continue
            pygame.draw.rect(screen, C_OPEN, cell_rect(*cell))
        for cell in algo.closed:
            if cell in (start, goal):
                continue
            pygame.draw.rect(screen, C_CLOSED, cell_rect(*cell))
        if algo.path:
            for cell in algo.path:
                if cell in (start, goal):
                    continue
                pygame.draw.rect(screen, C_PATH, cell_rect(*cell))
        if algo.current and not algo.finished and algo.current not in (start, goal):
            pygame.draw.rect(screen, C_CURRENT, cell_rect(*algo.current))

    # Muros
    for cell in walls:
        pygame.draw.rect(screen, C_WALL, cell_rect(*cell))

    # Inicio y meta encima de todo
    pygame.draw.rect(screen, C_START, cell_rect(*start))
    pygame.draw.rect(screen, C_GOAL, cell_rect(*goal))

    # Rejilla
    for r in range(ROWS):
        for c in range(COLS):
            pygame.draw.rect(screen, C_GRID, cell_rect(r, c), 1)


# ---------------- Bucle principal ----------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Visualizador A*")
    font = pygame.font.SysFont("consolas", 14, bold=True)
    clock = pygame.time.Clock()

    # Estado editable
    walls = set()
    start = (0, 0)
    goal = (ROWS - 1, COLS - 1)
    algo = AStarVisualizer(walls, start, goal)

    running = False
    speed = 20               # expansiones por segundo
    accumulator = 0.0
    dragging = None          # None | 'wall' | 'erase' | 'start' | 'goal'

    while True:
        dt = clock.tick(FPS) / 1000.0

        # -------- Eventos --------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
                elif event.key == pygame.K_SPACE:
                    if algo.finished:
                        algo.reset()
                        running = True
                    else:
                        running = not running
                elif event.key == pygame.K_s:
                    running = False
                    algo.step()
                elif event.key == pygame.K_r:
                    algo = AStarVisualizer(walls, start, goal)
                    running = False
                elif event.key == pygame.K_c:
                    walls.clear()
                    algo = AStarVisualizer(walls, start, goal)
                    running = False
                elif event.key == pygame.K_m:
                    walls.clear()
                    for r in range(ROWS):
                        for c in range(COLS):
                            if (r, c) in (start, goal):
                                continue
                            if random.random() < 0.25:
                                walls.add((r, c))
                    algo = AStarVisualizer(walls, start, goal)
                    running = False
                elif event.key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
                    speed = min(240, speed + 5)
                elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                    speed = max(1, speed - 5)

            if event.type == pygame.MOUSEBUTTONDOWN:
                cell = mouse_to_cell(event.pos)
                if cell is None:
                    continue
                if event.button == 1:
                    if cell == start:
                        dragging = 'start'
                    elif cell == goal:
                        dragging = 'goal'
                    elif cell not in walls:
                        walls.add(cell)
                        algo = AStarVisualizer(walls, start, goal)
                        running = False
                        dragging = 'wall'
                elif event.button == 3:
                    if cell in walls:
                        walls.discard(cell)
                        algo = AStarVisualizer(walls, start, goal)
                        running = False
                    dragging = 'erase'

            if event.type == pygame.MOUSEBUTTONUP:
                dragging = None

            if event.type == pygame.MOUSEMOTION and dragging:
                cell = mouse_to_cell(event.pos)
                if cell is None:
                    continue
                changed = False
                if dragging == 'start' and cell != goal and cell not in walls:
                    start = cell
                    changed = True
                elif dragging == 'goal' and cell != start and cell not in walls:
                    goal = cell
                    changed = True
                elif (dragging == 'wall' and cell not in (start, goal)
                        and cell not in walls):
                    walls.add(cell)
                    changed = True
                elif dragging == 'erase' and cell in walls:
                    walls.discard(cell)
                    changed = True
                if changed:
                    algo = AStarVisualizer(walls, start, goal)
                    running = False

        # -------- Avance del algoritmo --------
        if running and not algo.finished:
            accumulator += dt
            interval = 1.0 / speed
            while accumulator >= interval and not algo.finished:
                algo.step()
                accumulator -= interval
            if algo.finished:
                running = False

        # -------- Dibujo --------
        draw_scene(screen, font, algo, walls, start, goal, running, speed)
        pygame.display.flip()


if __name__ == "__main__":
    main()