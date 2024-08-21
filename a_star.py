import pygame
import math
from queue import PriorityQueue
from utils.vars import *


class Node:
    def __init__(self, row: int, col: int, width: int, total_rows: int) -> None:
        self.color = WHITE
        self.row = row
        self.col = col
        self.width = width
        self.x = row * width
        self.y = col * width
        self.neighbors = []
        self.total_rows = total_rows

    def get_pos(self) -> tuple[int, int]:
        return self.row, self.col

    def is_closed(self) -> bool:
        return self.color == RED

    def make_closed(self) -> None:
        self.color = RED

    def is_open(self) -> bool:
        return self.color == GREEN

    def make_open(self) -> None:
        self.color = GREEN

    def is_wall(self) -> bool:
        return self.color == BLACK

    def make_wall(self) -> None:
        self.color = BLACK

    def is_start(self) -> bool:
        return self.color == ORANGE

    def make_start(self) -> None:
        self.color = ORANGE

    def is_finish(self) -> bool:
        return self.color == TURQUOISE

    def make_finish(self) -> None:
        self.color = TURQUOISE

    def make_path(self) -> None:
        self.color = PURPLE

    def color_neighbors(self):
        self.color = PURPLE

    def reset(self) -> None:
        self.color = WHITE

    def draw(self, win: pygame.surface.Surface):
        pygame.draw.rect(surface=win, color=self.color, rect=(self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row > 0 and not grid[self.row - 1][self.col].is_wall():  # Down
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_wall():  # Up
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.col > 0 and not grid[self.row][self.col - 1].is_wall():  # Left
            self.neighbors.append(grid[self.row][self.col - 1])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_wall():  # Right
            self.neighbors.append(grid[self.row][self.col + 1])

    def __lt__(self, other):
        return False


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            n = Node(i, j, gap, rows)
            grid[i].append(n)

    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def a_star(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}

    g_score = {node: float('inf') for row in grid for node in row}
    g_score[start] = 0

    f_score = {node: float('inf') for row in grid for node in row}
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
            start.make_start()
            end.make_finish()
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

        draw()

        if current != start:
            current.make_closed()

    return None


def main(win, width):
    grid = make_grid(rows=ROWS, width=width)

    start = None
    end = None

    run = True
    started = False

    while run:
        draw(win, grid, ROWS, WIDTH)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]:
                # Left mouse click pressed
                # Add start, end, walls.
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                n = grid[row][col]
                if not start and n != end:
                    start = n
                    start.make_start()
                elif not end and n != start:
                    end = n
                    end.make_finish()
                elif n != start and n != end:
                    n.make_wall()

            elif pygame.mouse.get_pressed()[2]:
                # Right mouse click pressed. Remove start, end, walls.
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                n = grid[row][col]
                if n.is_start():
                    n.reset()
                    start = None
                elif n.is_finish():
                    n.reset()
                    end = None
                elif n.is_wall():
                    n.reset()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    a_star(lambda: draw(win, grid, ROWS, width), grid, start, end)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and not started:
                    for row in grid:
                        for node in row:
                            if node != start and node != end:
                                node.reset()

    pygame.quit()


if __name__ == '__main__':
    WIN = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption('A* Path Finder')

    main(win=WIN, width=WIDTH)