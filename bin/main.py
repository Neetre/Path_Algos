import pygame
import math
from queue import PriorityQueue
import time
import random

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

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
        self.weight = 1  # Default weight

    # Helper methods remain similar but use color dictionary
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
        self.weight = 5  # Higher weight for weighted nodes

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid, allow_diagonal=False):
        self.neighbors = []
        # Cardinal directions
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
    return abs(x1-x2) + abs(y1-y2)  # Manhattan


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


def algorithm(draw, grid, start, end, heuristic_type, speed, allow_diagonal):
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
            reconstruct_path(came_from, end, draw, start)  # Draw path
            end.make_end()
            elapsed = time.time() - start_time
            path_length = len(reconstruct_path(came_from, end, lambda: None, start, return_path=True))  # Get path length
            show_stats(elapsed, explored, path_length)
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + current.weight  # Include node weight
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + get_heuristic(
                    neighbor.get_pos(), end.get_pos(), heuristic_type)
                
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        if speed > 0:
            time.sleep(speed/1000)  # Controlled animation speed

        draw()

        if current != start:
            current.make_closed()

    show_stats(time.time()-start_time, explored, 0)
    return False

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


def draw(win, grid, rows, width):
	win.fill(COLORS["WHITE"])

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


def main(win, width):
    ROWS = 50  # Larger default grid
    grid = make_grid(ROWS, width)
    
    start = None
    end = None
    heuristic_type = "manhattan"
    speed = 10  # Animation speed
    allow_diagonal = False
    running = True

    while running:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if pygame.mouse.get_pressed()[0]:  # Left click
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
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:  # Add weight with shift
                        node.make_weight()
                    else:
                        node.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # Right click to clear
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start: start = None
                elif node == end: end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid, allow_diagonal)
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, 
                            start, end, heuristic_type, speed, allow_diagonal)
                
                if event.key == pygame.K_c:  # Clear
                    start = end = None
                    grid = make_grid(ROWS, width)
                
                if event.key == pygame.K_d:  # Toggle diagonal
                    allow_diagonal = not allow_diagonal
                    print(f"Diagonal movement: {allow_diagonal}")
                
                if event.key == pygame.K_h:  # Change heuristic
                    heuristics = ["manhattan", "euclidean", "chebyshev"]
                    current_idx = heuristics.index(heuristic_type)
                    heuristic_type = heuristics[(current_idx + 1) % 3]
                    print(f"Heuristic: {heuristic_type}")
                
                if event.key == pygame.K_s:  # Change speed
                    speed = (speed + 20) % 110
                    print(f"Animation speed: {speed}ms delay")
                
                if event.key == pygame.K_r:  # Random maze
                    generate_random_maze(grid, ROWS)

    pygame.quit()


def generate_random_maze(grid, rows):
    for row in grid:
        for node in row:
            node.reset()
            if random.random() < 0.25:  # 25% chance of barrier
                node.make_barrier()
            elif random.random() < 0.1:  # 10% chance of weight
                node.make_weight()
    

if __name__ == "__main__":
    main(WIN, WIDTH)
