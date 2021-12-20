import pygame
from queue import PriorityQueue
import Commons.Values as values


def reconstruct_path(came_from, current_node, draw):
    values.path_length_count = 0

    while current_node in came_from:
        current_node = came_from[current_node]
        current_node.make_path()
        values.path_length_count += 1
        draw()


def dijkstra_algo(draw, node_grid):
    start_node = values.start_node
    end_node = values.end_node

    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start_node))
    came_from = {}

    # Setting distance for all node to infinity
    distance = {spot: float("inf") for row in node_grid for spot in row}
    distance[start_node] = 0  # except start node

    open_set_hash = {start_node}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current_node = open_set.get()[2]
        open_set_hash.remove(current_node)

        if current_node == end_node:
            end_node.make_end()
            reconstruct_path(came_from, end_node, draw)
            start_node.make_start()
            return True

        for neighbor in current_node.neighbors:
            temp_distance = distance[current_node] + 1
            if temp_distance < distance[neighbor]:
                came_from[neighbor] = current_node
                distance[neighbor] = temp_distance

                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((distance[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
                    values.open_nodes_count = open_set.qsize()

        draw()

        if current_node != start_node:
            current_node.make_closed()
            if current_node.is_closed():
                values.closed_nodes_count += 1

    values.open_nodes_count = open_set.qsize()
    return False