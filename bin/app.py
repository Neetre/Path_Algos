from flask import Flask, request, jsonify, render_template
import json
import math
from queue import PriorityQueue
import time
import random
from main import Node, make_grid, algorithm, reconstruct_path

app = Flask(__name__)

# Define the Node class and other necessary functions from the original code here
# (You can copy the Node class, make_grid, algorithm, etc. from the original code)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/pathfind', methods=['POST'])
def pathfind():
    data = request.json
    grid_data = data['grid']
    start_pos = data['start']
    end_pos = data['end']
    heuristic_type = data.get('heuristic', 'manhattan')
    allow_diagonal = data.get('allow_diagonal', False)
    speed = data.get('speed', 10)

    # Convert grid data to Node objects
    rows = len(grid_data)
    grid = make_grid(rows, 800)
    for i in range(rows):
        for j in range(rows):
            if grid_data[i][j] == 'start':
                start = grid[i][j]
                start.make_start()
            elif grid_data[i][j] == 'end':
                end = grid[i][j]
                end.make_end()
            elif grid_data[i][j] == 'barrier':
                grid[i][j].make_barrier()
            elif grid_data[i][j] == 'weight':
                grid[i][j].make_weight()

    # Update neighbors
    for row in grid:
        for node in row:
            node.update_neighbors(grid, allow_diagonal)

    # Run the algorithm
    result = algorithm(lambda: None, grid, start, end, heuristic_type, speed, allow_diagonal)

    if result:
        came_from, end = result
        path = reconstruct_path(came_from, end, lambda: None, start, return_path=True)
        path_positions = [node.get_pos() for node in path]
        return jsonify({'status': 'success', 'path': path_positions})
    else:
        return jsonify({'status': 'failure', 'message': 'No path found'})

if __name__ == '__main__':
    app.run(debug=True)