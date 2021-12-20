import pygame
import Commons.Constants as const


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = const.DEFAULT_COLOR
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == const.COLSED_COLOR

    def is_open(self):
        return self.color == const.OPEN_COLOR

    def is_barrier(self):
        return self.color == const.BARRIER_COLOR

    def is_start(self):
        return self.color == const.START_COLOR

    def is_end(self):
        return self.color == const.END_COLOR

    def is_path(self):
        return self.color == const.PATH_COLOR

    def reset(self):
        self.color = const.DEFAULT_COLOR

    def make_start(self):
        self.color = const.START_COLOR

    def make_closed(self):
        self.color = const.COLSED_COLOR

    def make_open(self):
        self.color = const.OPEN_COLOR

    def make_barrier(self):
        self.color = const.BARRIER_COLOR

    def make_end(self):
        self.color = const.END_COLOR

    def make_path(self):
        self.color = const.PATH_COLOR

    def draw(self, win):
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, node_grid):
        self.neighbors = []

        # RIGHT
        if self.col < self.total_rows - 1 and not node_grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(node_grid[self.row][self.col + 1])

        # UP
        if self.row > 0 and not node_grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(node_grid[self.row - 1][self.col])

        # LEFT
        if self.col > 0 and not node_grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(node_grid[self.row][self.col - 1])

        # DOWN
        if self.row < self.total_rows - 1 and not node_grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(node_grid[self.row + 1][self.col])


    def __lt__(self, other):
        return False

