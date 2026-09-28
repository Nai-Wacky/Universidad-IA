import pygame
import heapq

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
C_OPEN    = (255, 176, 59)
C_CLOSED  = (116, 185, 255)
C_CURRENT = (255, 105, 180)
C_PATH    = (255, 224, 102)
C_TEXT    = (230, 230, 230)

# Inicio y meta fijos (se cambian aquí)
START = (0, 0)
GOAL  = (ROWS - 1, COLS - 1)


# ---------------- A* instrumentado ----------------
class AStarVisualizer:
    def __init__(self, walls):
        self.walls = walls
        self.start = START
        self.goal = GOAL
        self.reset()

    def reset(self):
        self.open_heap = []
        self.g_score = {self.start: 0}
        self.came_from = {}
        self.closed = set()
        self.current = None
        self.path = None
        self.finished = False
        heapq.heappush(self.open_heap, (self._h(self.start), 0, self.start))

    def _h(self, a):
        return abs(a[0] - self.goal[0]) + abs(a[1] - self.goal[1])

    def _neighbors(self, pos):
        r, c = pos
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS and (nr, nc) not in self.walls:
                yield (nr, nc)

    def step(self):
        if self.finished:
            return
        while self.open_heap:
            f, g, current = heapq.heappop(self.open_heap)
            if current in self.closed:
                continue

            self.closed.add(current)
            self.current = current

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

            for nxt in self._neighbors(current):
                new_g = self.g_score[current] + 1
                if nxt not in self.g_score or new_g < self.g_score[nxt]:
                    self.g_score[nxt] = new_g
                    self.came_from[nxt] = current
                    heapq.heappush(
                        self.open_heap, (new_g + self._h(nxt), new_g, nxt)
                    )
            return
        self.finished = True


# ---------------- Helpers ----------------
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


def draw_scene(screen, font, algo, walls, running):
    screen.fill(C_BG)

    # Cabecera con instrucciones
    info = "ESPACIO:play/pause   R:reset   C:limpiar   clic:dibujar   clic-dcho:borrar"
    screen.blit(font.render(info, True, C_TEXT), (8, 16))

    # Celdas vacías
    for r in range(ROWS):
        for c in range(COLS):
            pygame.draw.rect(screen, C_EMPTY, cell_rect(r, c))

    # Frontera (en open, sin expandir)
    open_set = set(algo.g_score.keys()) - algo.closed
    for cell in open_set:
        if cell in (START, GOAL):
            continue
        pygame.draw.rect(screen, C_OPEN, cell_rect(*cell))

    # Cerrados
    for cell in algo.closed:
        if cell in (START, GOAL):
            continue
        pygame.draw.rect(screen, C_CLOSED, cell_rect(*cell))

    # Camino final
    if algo.path:
        for cell in algo.path:
            if cell in (START, GOAL):
                continue
            pygame.draw.rect(screen, C_PATH, cell_rect(*cell))

    # Nodo actual
    if algo.current and not algo.finished and algo.current not in (START, GOAL):
        pygame.draw.rect(screen, C_CURRENT, cell_rect(*algo.current))

    # Muros
    for cell in walls:
        pygame.draw.rect(screen, C_WALL, cell_rect(*cell))

    # Inicio y meta
    pygame.draw.rect(screen, C_START, cell_rect(*START))
    pygame.draw.rect(screen, C_GOAL, cell_rect(*GOAL))

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

    walls = set()
    algo = AStarVisualizer(walls)
    running = False
    speed = 20
    accumulator = 0.0

    while True:
        dt = clock.tick(FPS) / 1000.0

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
                    running = not running
                elif event.key == pygame.K_r:
                    algo.reset()
                    running = False
                elif event.key == pygame.K_c:
                    walls.clear()
                    algo = AStarVisualizer(walls)
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                cell = mouse_to_cell(event.pos)
                if cell and cell not in (START, GOAL):
                    if event.button == 1 and cell not in walls:
                        walls.add(cell)
                        algo = AStarVisualizer(walls)
                        running = False
                    elif event.button == 3 and cell in walls:
                        walls.discard(cell)
                        algo = AStarVisualizer(walls)
                        running = False

        if running and not algo.finished:
            accumulator += dt
            interval = 1.0 / speed
            while accumulator >= interval and not algo.finished:
                algo.step()
                accumulator -= interval
            if algo.finished:
                running = False

        draw_scene(screen, font, algo, walls, running)
        pygame.display.flip()


if __name__ == "__main__":
    main()