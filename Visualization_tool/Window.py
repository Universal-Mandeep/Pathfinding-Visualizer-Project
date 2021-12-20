import pygame
import Commons.Constants as const
import Commons.Values as values
import Visualization_tool.NODE
import Visualization_tool.BUTTON
import Algos.A_Star
import Algos.Dijkstra
import Algos.Best_first_search
pygame.font.init()

def make_window():
    WIN = pygame.display.set_mode((const.WIDTH, const.GRID_HEIGHT))
    pygame.display.set_caption("Path Finding Visualizer")
    return WIN


# calling this function in draw function ... to update all buttons
def update_buttons(win):
    for button in values.button_grid:
        button.draw_button(win)


def make_button(win):
    a_star_algo_button = Visualization_tool.BUTTON.Button((const.GRID_WIDTH, 0), const.BUTTON_SIZE, "A* Algorithm")
    a_star_algo_button.draw_button(win)

    dijkstra_algo_button = Visualization_tool.BUTTON.Button((const.GRID_WIDTH, 50), const.BUTTON_SIZE, "Dijkstra's Algorithm")
    dijkstra_algo_button.draw_button(win)

    best_first_search_button = Visualization_tool.BUTTON.Button((const.GRID_WIDTH, 100), const.BUTTON_SIZE, "Best First Search Algorithm")
    best_first_search_button.draw_button(win)

    values.button_grid.append(a_star_algo_button)
    values.button_grid.append(dijkstra_algo_button)
    values.button_grid.append(best_first_search_button)


    # Setting A* Algorithm as default seleted algorithm
    a_star_algo_button.make_selected()
    values.algo_button = a_star_algo_button


def reset_stat():
    values.unvisited_nodes_count = 0
    values.barrier_count = 0
    values.open_nodes_count = 0
    values.closed_nodes_count = 0
    values.path_length_count = 0


def update_stat(win):
    pygame.draw.rect(win, const.STAT_BACKGROUND_COLOR, (const.GRID_WIDTH, 450, const.DISPLAY_WIDTH, 500))
    
    barrier_count_label = const.MAIN_FONT.render(f"Barrier Count: {values.barrier_count}", 1, const.FONT_COLOR)
    values.unvisited_nodes_count = (const.TOTAL_ROWS * const.TOTAL_ROWS) - values.open_nodes_count - values.closed_nodes_count - values.barrier_count
    unvisited_nodes_count_label = const.MAIN_FONT.render(f"Unvisited Node Count: {values.unvisited_nodes_count}", 1, const.FONT_COLOR)
    open_node_count_label = const.MAIN_FONT.render(f"Open Node Count: {values.open_nodes_count}", 1, const.FONT_COLOR)
    closed_node_count_label = const.MAIN_FONT.render(f"Closed Node Count: {values.closed_nodes_count}", 1, const.FONT_COLOR)
    path_length_count_label = const.MAIN_FONT.render(f"Path Length Count: {values.path_length_count}", 1, const.FONT_COLOR)

    win.blit(unvisited_nodes_count_label, (const.GRID_WIDTH + 50, 450))
    win.blit(barrier_count_label, (const.GRID_WIDTH + 50, 500))
    win.blit(open_node_count_label, (const.GRID_WIDTH + 50, 550))
    win.blit(closed_node_count_label, (const.GRID_WIDTH + 50, 600))
    win.blit(path_length_count_label, (const.GRID_WIDTH + 50, 650))


# Clearing warning msg
def clear_warning_msg(win):
    pygame.draw.rect(win, const.STAT_BACKGROUND_COLOR, (const.GRID_WIDTH, 300, const.DISPLAY_WIDTH, 50))


def pop_warning(win):
    clear_warning_msg(win)
    warning_label = const.MAIN_FONT.render("NO POSSIBLE PATH", 1, (252, 252, 54))
    warning_label_width = warning_label.get_width()
    warning_label_margin = const.DISPLAY_WIDTH - warning_label_width
    win.blit(warning_label, (const.GRID_WIDTH + (warning_label_margin/2), 300))


def make_grid():
    values.node_grid = []
    gap = const.GRID_WIDTH // const.TOTAL_ROWS
    for i in range(const.TOTAL_ROWS):
        values.node_grid.append([])
        for j in range(const.TOTAL_ROWS):
            node = Visualization_tool.NODE.Node(i, j, gap, const.TOTAL_ROWS)
            values.node_grid[i].append(node)
    return values.node_grid


def draw_grid(win):   # Drawing all the updates
    gap = const.GRID_WIDTH // const.TOTAL_ROWS
    for i in range(const.TOTAL_ROWS):
        pygame.draw.line(win, const.GRID_LINE_COLOR, (0, i * gap), (const.GRID_WIDTH, i * gap))
        for j in range(const.TOTAL_ROWS):
            pygame.draw.line(win, const.GRID_LINE_COLOR, (j * gap, 0), (j * gap, const.GRID_WIDTH))


def draw_nodes(win, grid):
    for row in grid:
        for node in row:
            node.draw(win)


def draw(win, grid):
    draw_nodes(win, grid)
    draw_grid(win)
    update_buttons(win)
    update_stat(win)
    pygame.display.update()


def clear_screen_for_reset(node_grid):
    for row in node_grid:
        for node in row:
            if node.is_open() or node.is_closed() or node.is_path():
                node.reset()


def get_clicked_pos(pos):
    gap = const.GRID_WIDTH // const.TOTAL_ROWS
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def check_events(win, node_grid):
    for event in pygame.event.get():
        # QUIT EVENT
        if event.type == pygame.QUIT:
            const.RUN_PROGRAM = False
        
        # LEFT MOUSE BUTTON
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            # pos is a tuple in the form (y, x)
            
            # Left click function in grid   -> to set a node
            if(pos[0] < const.GRID_WIDTH):
                row, col = get_clicked_pos(pos)
                Node = node_grid[row][col]
            
                if not values.start_node and Node != values.end_node:
                    values.start_node = Node
                    Node.make_start()
            
                elif not values.end_node and Node != values.start_node:
                    values.end_node = Node
                    Node.make_end()

                elif Node != values.end_node and Node != values.start_node:
                    if not Node.is_barrier():
                        values.barrier_count += 1
                        Node.make_barrier()

            # Left click function in display window   -> to select the algo button
            if((pos[0] > const.GRID_WIDTH and pos[0] < const.WIDTH) and (pos[1] > 0 and pos[1] < (values.button_grid.__len__() * const.BUTTON_HEIGHT))):
                button_number = pos[1] // const.BUTTON_HEIGHT
                clicked_button = values.button_grid[button_number]

                if values.algo_button != clicked_button:
                    # First unselecting the selected button and making newly clicked as selected
                    values.algo_button.make_unselected()
                    clicked_button.make_selected()
                    values.algo_button = clicked_button
                    #reset_stat()


        # RIGHT MOUSE BUTTON
        elif pygame.mouse.get_pressed()[2]:
            pos = pygame.mouse.get_pos()
            # pos is a tuple
        
            # Right click function in grid    -> to remove a node
            if(pos[0] < const.GRID_WIDTH):
                row, col = get_clicked_pos(pos)
                Node = node_grid[row][col]

                # reducing barrier count by 1
                if Node.is_barrier():
                    values.barrier_count -= 1

                if Node == values.start_node:
                    values.start_node = None
                elif Node == values.end_node:
                    values.end_node = None

                Node.reset()



        # WHEN KEYBOARD KEY IS PRESSED
        if event.type == pygame.KEYDOWN:
            # SPACE BAR    -> TO START THE ALGO
            if event.key == pygame.K_SPACE and values.start_node and values.end_node:
                for row in node_grid:
                    for Node in row:
                        Node.update_neighbors(node_grid)

                # Resetting statistic values and clearing warning(if any) before starting the function
                values.path_length_count = 0
                values.open_nodes_count = 0
                values.closed_nodes_count = 0
                clear_warning_msg(win)
                clear_screen_for_reset(node_grid)


                # sync the algo with corresponding selected button
                if values.algo_button.get_text() == "A* Algorithm":
                    if not Algos.A_Star.a_star_algo(lambda: draw(win, node_grid), node_grid):
                        pop_warning(win)
                    # if Algos.A_Star.a_star_algo(lambda: draw(win, node_grid), node_grid):
                    #     print("Node found ... a star")
                    # else:
                    #     pop_warning(win)
                elif values.algo_button.get_text() == "Dijkstra's Algorithm":
                    if not Algos.Dijkstra.dijkstra_algo(lambda: draw(win, node_grid), node_grid):
                        pop_warning(win)

                elif values.algo_button.get_text() == "Best First Search Algorithm":
                    if not Algos.Best_first_search.best_first_search_algo(lambda: draw(win, node_grid), node_grid):
                        pop_warning(win)

                
                #Algos.A_Star.a_star_algo(lambda: draw(win, node_grid), node_grid, values.start_node, values.end_node)
                #Algos.Dijkstra.dijkstra_algo(lambda: draw(win, node_grid), node_grid, values.start_node, values.end_node)
                #Algos.BFS.bfs_algo(lambda: draw(win, node_grid), node_grid, values.start_node, values.end_node)

            if event.key == pygame.K_c:
                values.start_node = None
                values.end_node = None
                values.node_grid = make_grid()

                reset_stat()
                #values.barrier_count = 0
