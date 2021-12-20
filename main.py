import pygame
import Visualization_tool.NODE as Node
import Visualization_tool.Window as WIN
import Commons.Constants as const
import Commons.Values as values

Window = WIN.make_window()


def main(Window):
    values.node_grid = WIN.make_grid()
    WIN.make_button(Window)

    while const.RUN_PROGRAM:
        WIN.draw(Window, values.node_grid)
        WIN.check_events(Window, values.node_grid)

    pygame.quit()

if __name__ == "__main__":
    main(Window)