import pygame
import math
from queue import PriorityQueue
import time
import random

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Path Finding Algorithms")
pygame.init()


COLORS = {
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    "YELLOW": (255, 255, 0),
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),
    "PURPLE": (128, 0, 128),
    "ORANGE": (255, 165, 0),
    "GREY": (128, 128, 128),
    "TURQUOISE": (64, 224, 208),
    "DARK_GREY": (50, 50, 50),
    "WEIGHT": (139, 69, 19)
}

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = COLORS["WHITE"]
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        self.weight = 1

    def get_pos(self): return (self.row, self.col)
    def is_closed(self): return self.color == COLORS["RED"]
    def is_open(self): return self.color == COLORS["GREEN"]
    def is_barrier(self): return self.color == COLORS["BLACK"]
    def is_start(self): return self.color == COLORS["ORANGE"]
    def is_end(self): return self.color == COLORS["TURQUOISE"]
    def is_weight(self): return self.color == COLORS["WEIGHT"]
    
    def reset(self):
        self.color = COLORS["WHITE"]
        self.weight = 1

    def make_start(self): self.color = COLORS["ORANGE"]
    def make_closed(self): self.color = COLORS["RED"]
    def make_open(self): self.color = COLORS["GREEN"]
    def make_barrier(self): self.color = COLORS["BLACK"]
    def make_end(self): self.color = COLORS["TURQUOISE"]
    def make_path(self): self.color = COLORS["PURPLE"]
    def make_weight(self): 
        self.color = COLORS["WEIGHT"]
        self.weight = 5

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid, allow_diagonal=False):
        self.neighbors = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        if allow_diagonal:
            directions += [(1, 1), (-1, -1), (1, -1), (-1, 1)]
        
        for dr, dc in directions:
            new_row = self.row + dr
            new_col = self.col + dc
            if 0 <= new_row < self.total_rows and 0 <= new_col < self.total_rows:
                neighbor = grid[new_row][new_col]
                if not neighbor.is_barrier():
                    self.neighbors.append(neighbor)

    def __lt__(self, other): return False


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def get_heuristic(p1, p2, heuristic_type="manhattan"):
    x1, y1 = p1
    x2, y2 = p2
    if heuristic_type == "euclidean":
        return math.hypot(x1-x2, y1-y2)
    elif heuristic_type == "chebyshev":
        return max(abs(x1-x2), abs(y1-y2))
    return abs(x1-x2) + abs(y1-y2)


def reconstruct_path(came_from, current, draw, start, return_path=False):
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.reverse()
    
    if return_path:
        return path
    
    for node in path:
        if node != start and not node.is_end():
            node.make_path()
            draw()
    return path


def a_star(draw, grid, start, end, heuristic_type, speed, allow_diagonal):
    start_time = time.time()
    open_set = PriorityQueue()
    open_set.put((0, 0, start))
    came_from = {}
    
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = get_heuristic(start.get_pos(), end.get_pos(), heuristic_type)
    
    open_set_hash = {start}
    count = 1
    explored = 0

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        current = open_set.get()[2]
        open_set_hash.remove(current)
        explored += 1

        if current == end:
            reconstruct_path(came_from, end, draw, start)
            end.make_end()
            elapsed = time.time() - start_time
            path_length = len(reconstruct_path(came_from, end, lambda: None, start, return_path=True))
            show_stats(elapsed, explored, path_length)
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + current.weight
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + get_heuristic(neighbor.get_pos(), end.get_pos(), heuristic_type)
                
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        if speed > 0:
            time.sleep(speed/1000)

        draw()

        if current != start:
            current.make_closed()

    show_stats(time.time()-start_time, explored, 0)
    return False


def dijkstra(draw, grid, start, end, speed):
    start_time = time.time()
    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    
    open_set_hash = {start}
    explored = 0

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        current = open_set.get()[1]
        open_set_hash.remove(current)
        explored += 1

        if current == end:
            reconstruct_path(came_from, end, draw, start)
            end.make_end()
            elapsed = time.time() - start_time
            path_length = len(reconstruct_path(came_from, end, lambda: None, start, return_path=True))
            show_stats(elapsed, explored, path_length)
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + current.weight
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                
                if neighbor not in open_set_hash:
                    open_set.put((g_score[neighbor], neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        if speed > 0:
            time.sleep(speed/1000)

        draw()

        if current != start:
            current.make_closed()

    show_stats(time.time()-start_time, explored, 0)
    return False


def greedy_best_first(draw, grid, start, end, heuristic_type, speed):
    start_time = time.time()
    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    
    open_set_hash = {start}
    explored = 0

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        current = open_set.get()[1]
        open_set_hash.remove(current)
        explored += 1

        if current == end:
            reconstruct_path(came_from, end, draw, start)
            end.make_end()
            elapsed = time.time() - start_time
            path_length = len(reconstruct_path(came_from, end, lambda: None, start, return_path=True))
            show_stats(elapsed, explored, path_length)
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + current.weight
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                
                if neighbor not in open_set_hash:
                    f_score = get_heuristic(neighbor.get_pos(), end.get_pos(), heuristic_type)
                    open_set.put((f_score, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        if speed > 0:
            time.sleep(speed/1000)

        draw()

        if current != start:
            current.make_closed()

    show_stats(time.time()-start_time, explored, 0)
    return False


def algorithm(draw, grid, start, end, heuristic_type, speed, allow_diagonal, algorithm_type="a_star"):
    if algorithm_type == "dijkstra":
        return dijkstra(draw, grid, start, end, speed)
    elif algorithm_type == "greedy":
        return greedy_best_first(draw, grid, start, end, heuristic_type, speed)
    else:
        return a_star(draw, grid, start, end, heuristic_type, speed, allow_diagonal)


def show_stats(time_taken, nodes_explored, path_length):
    print(f"\n--- Statistics ---")
    print(f"Time taken: {time_taken:.2f}s")
    print(f"Nodes explored: {nodes_explored}")
    print(f"Path length: {path_length}")
    print(f"------------------")


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, COLORS["GREY"], (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, COLORS["GREY"], (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width, command_window):
    win.fill(COLORS["WHITE"])

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)

    command_surface = command_window.draw_commands()
    win.blit(command_surface, (width, 0))
    
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col


class CommandWindow:
    def __init__(self):
        self.width = 400
        self.height = 800
        self.window = pygame.display.set_mode((WIDTH + self.width, WIDTH))
        pygame.display.set_caption("Path Finding Algorithms")
        
    def draw_commands(self):
        command_surface = pygame.Surface((self.width, WIDTH))
        command_surface.fill(COLORS["WHITE"])

        font_title = pygame.font.SysFont("arial", 24, bold=True)
        title = font_title.render("Commands", True, COLORS["BLACK"])
        command_surface.blit(title, (10, 20))

        font = pygame.font.SysFont("arial", 18)
        commands = [
            ("Controls:", ""),
            ("Left Click", "Place Start/End/Barrier"),
            ("Shift + Left Click", "Place Weight (cost=5)"),
            ("Right Click", "Clear Node"),
            ("Space", "Start Algorithm"),
            ("", ""),
            ("Algorithms:", ""),
            ("1", "A* Algorithm"),
            ("2", "Dijkstra's Algorithm"),
            ("3", "Greedy Best-First Search"),
            ("", ""),
            ("Options:", ""),
            ("C", "Clear Grid"),
            ("D", "Toggle Diagonal Movement"),
            ("H", "Change Heuristic"),
            ("S", "Change Speed"),
            ("R", "Generate Random Maze")
        ]
        
        y_offset = 60
        line_spacing = 25
        
        for key, description in commands:
            if key == "": 
                y_offset += line_spacing // 2
                continue
                
            if key.endswith(":"):
                y_offset += line_spacing // 2
                text = font.render(key, True, COLORS["DARK_GREY"])
                command_surface.blit(text, (10, y_offset))
            else:
                key_surface = pygame.font.SysFont("arial", 18, bold=True).render(key, True, COLORS["BLACK"])
                command_surface.blit(key_surface, (10, y_offset))

                desc_surface = font.render(description, True, COLORS["BLACK"])
                command_surface.blit(desc_surface, (130, y_offset))
            
            y_offset += line_spacing

        pygame.draw.line(command_surface, COLORS["GREY"], (0, 0), (0, WIDTH), 2)
        
        return command_surface


def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)
    command_window = CommandWindow()
    
    start = None
    end = None
    heuristic_type = "manhattan"
    speed = 10
    allow_diagonal = False
    algorithm_type = "a_star"
    running = True

    while running:
        draw(win, grid, ROWS, width, command_window)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()
                elif not end and node != start:
                    end = node
                    end.make_end()
                elif node != start and node != end:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        node.make_weight()
                    else:
                        node.make_barrier()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid, allow_diagonal)
                    algorithm(lambda: draw(win, grid, ROWS, width, command_window), grid, 
                            start, end, heuristic_type, speed, allow_diagonal, algorithm_type)

                if event.key == pygame.K_c:
                    start = end = None
                    grid = make_grid(ROWS, width)

                if event.key == pygame.K_d:
                    allow_diagonal = not allow_diagonal
                    print(f"Diagonal movement: {allow_diagonal}")

                if event.key == pygame.K_h:
                    heuristics = ["manhattan", "euclidean", "chebyshev"]
                    current_idx = heuristics.index(heuristic_type)
                    heuristic_type = heuristics[(current_idx + 1) % 3]
                    print(f"Heuristic: {heuristic_type}")

                if event.key == pygame.K_s:
                    speed = (speed + 20) % 110
                    print(f"Animation speed: {speed}ms delay")

                if event.key == pygame.K_r:
                    generate_random_maze(grid, ROWS)

                if event.key == pygame.K_1:
                    algorithm_type = "a_star"
                    print("Algorithm: A*")

                if event.key == pygame.K_2:
                    algorithm_type = "dijkstra"
                    print("Algorithm: Dijkstra")

                if event.key == pygame.K_3:
                    algorithm_type = "greedy"
                    print("Algorithm: Greedy Best-First Search")

    pygame.quit()

def generate_random_maze(grid, rows):
    for row in grid:
        for node in row:
            node.reset()
            if random.random() < 0.25:
                node.make_barrier()
            elif random.random() < 0.1:
                node.make_weight()

if __name__ == "__main__":
    main(WIN, WIDTH)
