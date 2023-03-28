from queue import PriorityQueue
from utils import Euclidean


def astar(start, goal, graph):
    # Initialize start node
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[str(start)] = None
    cost_so_far[str(start)] = 0

    # Run search algorithm
    while not frontier.empty():
        current = frontier.get()

        # Goal reached
        if current == goal:
            break

        # Explore neighbors
        for neighbor in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, neighbor)
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + Euclidean(goal, neighbor)
                frontier.put(neighbor, priority)
                came_from[neighbor] = current

    return came_from, cost_so_far
