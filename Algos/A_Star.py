import pygame
from queue import PriorityQueue
import Commons.Values as values


def heuristic(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current_node, draw):
    # Reseting path length count value
    values.path_length_count = 0
    while current_node in came_from:
        current_node = came_from[current_node]
        current_node.make_path()
        values.path_length_count += 1
        draw()


def a_star_algo(draw, node_grid):
    start_node = values.start_node
    end_node = values.end_node

    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start_node))
    came_from = {}

    # Setting g score of all node to infinity
    g_score = {spot: float("inf") for row in node_grid for spot in row}
    g_score[start_node] = 0  # except start node
    
    f_score = {spot: float("inf") for row in node_grid for spot in row}
    f_score[start_node] = heuristic(start_node.get_pos(), end_node.get_pos())

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
            temp_g_score = g_score[current_node] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current_node
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor.get_pos(), end_node.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

                    # Updating open node count when a node is made open
                    # It also count the start node which is always open
                    values.open_nodes_count = open_set.qsize()

        draw()

        if current_node != start_node:
            current_node.make_closed()
            if current_node.is_closed():
                values.closed_nodes_count += 1

    values.open_nodes_count = open_set.qsize()
    return False
