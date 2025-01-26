class PriorityQueue {
    constructor() {
        this.elements = [];
    }

    enqueue(element, priority) {
        this.elements.push({ element, priority });
        this.elements.sort((a, b) => a.priority - b.priority);
    }

    dequeue() {
        return this.elements.shift();
    }

    isEmpty() {
        return this.elements.length === 0;
    }
}

function aStar(graph, start, target, heuristic) {
    const openSet = new PriorityQueue();
    const cameFrom = {};
    const gScore = {};
    const fScore = {};

    // Initialize scores
    for (const node in graph) {
        gScore[node] = Infinity;
        fScore[node] = Infinity;
    }
    gScore[start] = 0;
    fScore[start] = heuristic(start, target);
    openSet.enqueue(start, fScore[start]);

    while (!openSet.isEmpty()) {
        const { element: current } = openSet.dequeue();

        if (current === target) {
            // Reconstruct path
            const path = [current];
            let node = current;
            while (cameFrom[node] !== undefined) {
                node = cameFrom[node];
                path.unshift(node);
            }
            return path;
        }

        for (const neighbor of graph[current]) {
            const tentativeGScore = gScore[current] + neighbor.weight;
            if (tentativeGScore < gScore[neighbor.node]) {
                cameFrom[neighbor.node] = current;
                gScore[neighbor.node] = tentativeGScore;
                fScore[neighbor.node] = tentativeGScore + heuristic(neighbor.node, target);
                openSet.enqueue(neighbor.node, fScore[neighbor.node]);
            }
        }
    }
    return null; // No path exists
}