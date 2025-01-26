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

function dijkstra(graph, start, target) {
    const distances = {};
    const prev = {};
    const pq = new PriorityQueue();

    // Initialize distances and priority queue
    for (const node in graph) {
        distances[node] = Infinity;
    }
    distances[start] = 0;
    pq.enqueue(start, 0);

    while (!pq.isEmpty()) {
        const { element: current } = pq.dequeue();

        if (current === target) {
            // Reconstruct path
            const path = [];
            let node = target;
            while (node !== start) {
                path.unshift(node);
                node = prev[node];
            }
            path.unshift(start);
            return { path, distance: distances[target] };
        }

        for (const neighbor of graph[current]) {
            const alt = distances[current] + neighbor.weight;
            if (alt < distances[neighbor.node]) {
                distances[neighbor.node] = alt;
                prev[neighbor.node] = current;
                pq.enqueue(neighbor.node, alt);
            }
        }
    }
    return null; // No path exists
}