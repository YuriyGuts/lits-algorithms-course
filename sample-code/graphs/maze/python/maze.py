import random
import time

from Tkinter import *


def main():
    height = 25
    width = 40
    maze_cell_size = 25
    animation_delay = 0.005

    def begin_simulation():
        def on_cell_created(new_cell, previous_cell):
            ui.draw_cell(new_cell)
            if previous_cell is not None:
                ui.draw_cell(previous_cell)
            ui.do_animation_delay()

        def on_cell_solved(cell, step_count):
            ui.draw_cell(cell, color=UI.color_solved_cell_background, text=str(step_count))
            ui.do_animation_delay()

        def on_exit_path_updated(cell, previous_cell):
            ui.draw_trace(cell, previous_cell)
            ui.do_animation_delay()

        # Generate a perfect maze (the one that has a unique path between every two cells).
        maze = generate_maze(height, width, on_cell_created)

        # Make the maze more interesting by removing random walls, thus producing alternative paths.
        remove_random_walls(maze, wall_count=height * width / 15)
        ui.draw_maze(maze)

        # Calculate shortest paths to every cell and backtrace the path between start and end.
        path_lengths, exit_path = solve_maze(maze, on_cell_solved, on_exit_path_updated)

    ui = UI(height, width, maze_cell_size, animation_delay)
    ui.set_action_for_go_button(begin_simulation)
    ui.run()


def generate_maze(height, width, cell_created_callback=None):
    maze = Maze(height, width)

    # Just doing the typical DFS: putting the start cell in the stack.
    # But in order to generate a maze, we'll also remember the cell we came from.
    # Whenever we process a new cell, we'll break the wall between the current cell
    # and the cell we came from. Therefore, we'll need to store multiple values in one stack item.
    start_cell = maze.get_cell_by_coordinate(0, 0)
    previous_cell = None

    stack = [(start_cell, previous_cell)]
    visited = [
        [False for x in range(0, width)]
        for y in range(0, height)
    ]

    while len(stack) > 0:
        # Retrieve another pair of cells from the stack.
        current_cell, previous_cell = stack.pop()

        # Ignoring the cell if we've already been there.
        if visited[current_cell.y][current_cell.x]:
            continue

        # Mark this cell so we won't visit it anymore.
        visited[current_cell.y][current_cell.x] = True

        # Break the wall between the current cell and the previous cell.
        if previous_cell is not None:
            maze.break_wall_between_cells(previous_cell, current_cell)

            # Notify the UI that we've created a new cell.
            if cell_created_callback is not None:
                cell_created_callback(current_cell, previous_cell)

        # Get all neighbors that are within the bounds of the maze and have all 4 walls intact.
        neighbors = maze.get_adjacent_cells(current_cell)
        unvisited_neighbors = list([
            neighbor
            for neighbor in neighbors
            if not visited[neighbor.y][neighbor.x] and neighbor.has_all_walls()
        ])

        # Shuffle the neighbors so that we visit them in random order.
        # That will make our maze much more interesting.
        random.shuffle(unvisited_neighbors)
        stack.extend([
            (neighbor, current_cell) for neighbor in unvisited_neighbors
        ])

    return maze


def solve_maze(maze, cell_solved_callback=None, exit_path_updated_callback=None):
    # Just doing the typical BFS, but, in addition to the cell itself,
    # we'll also store the length of the (start -> cell) path in the queue.
    # Because it's BFS and the graph is not weighted, the path length will
    # also be the MINIMUM path length. Obviously, the length is 0 for the start cell.
    start_cell = maze.get_cell_by_coordinate(0, 0)
    steps_taken = 0

    queue = [(start_cell, steps_taken)]
    visited = [
        [False for x in range(0, maze.width)]
        for y in range(0, maze.height)
    ]

    # Remembering the shortest path lengths for every cell in the maze.
    # Initially, we don't know any shortest paths, so it's None for every cell.
    path_lengths = [
        [None for x in range(0, maze.width)]
        for y in range(0, maze.height)
    ]

    while len(queue) > 0:
        # Fetch the next (cell, steps) pair from the queue.
        current_cell, steps_taken = queue.pop(0)

        # If we've already analyzed this cell, ignore it completely.
        if visited[current_cell.y][current_cell.x]:
            continue

        # Mark the cell as visited so that we won't visit it anymore.
        visited[current_cell.y][current_cell.x] = True
        path_lengths[current_cell.y][current_cell.x] = steps_taken

        # Notify the UI that we've solved a new cell.
        if cell_solved_callback is not None:
            cell_solved_callback(current_cell, steps_taken)

        # Discovering the unvisited neighbors that are reachable from the current_cell
        # (the ones that don't have walls between them and our cell).
        unvisited_neighbors = [
            neighbor
            for neighbor in maze.get_adjacent_reachable_cells(current_cell)
            if not visited[neighbor.y][neighbor.x]
        ]

        # Every neighbor will have a (moves + 1) minimum path length.
        queue.extend([
            (neighbor, steps_taken + 1)
            for neighbor in unvisited_neighbors
        ])

    # Now that we've computed the matrix of all shortest path lengths,
    # we can reconstruct the path from the end cell to the start cell.
    exit_path = trace_exit_path(
        maze,
        path_lengths,
        maze.get_cell_by_coordinate(0, 0),
        maze.get_cell_by_coordinate(maze.height - 1, maze.width - 1)
    )

    # Notify the UI that we've traced one more cell from the exit path.
    if exit_path_updated_callback is not None:
        for i in range(1, len(exit_path)):
            exit_path_updated_callback(exit_path[i], exit_path[i - 1])

    return path_lengths, exit_path


def remove_random_walls(maze, wall_count):
    suitable_cells_for_removal = []

    for y in range(1, maze.height - 2):
        x = 1
        while x < maze.width - 2:
            # If there's a horizontal wall that spans 3 consecutive cells,
            # we're safe to remove the middle wall without introducing any open areas:
            #
            #   ..........        ..........
            #   .  .  .  .        .  .  .  .
            #   ==========   ->   ===....===
            #   .  .  .  .        .  .  .  .
            #   ..........        ..........
            #
            cell = maze.get_cell_by_coordinate(y, x)
            if cell.has_wall(0) and maze.cells[y][x - 1].has_wall(0) and maze.cells[y][x + 1].has_wall(0):
                suitable_cells_for_removal.append(cell)
                x += 2
            else:
                x += 1

    random.shuffle(suitable_cells_for_removal)
    remove_list = suitable_cells_for_removal[:wall_count]

    for cell in remove_list:
        north_neighbor = maze.get_cell_by_coordinate(cell.y - 1, cell.x)
        maze.break_wall_between_cells(cell, north_neighbor)


def trace_exit_path(maze, path_lengths, start_cell, exit_cell):
    path = [exit_cell]
    current_cell = exit_cell

    # At each step, move to any neighbor cell that has a path length of (steps - 1)
    # until we reach the start cell.
    while not (current_cell.y == start_cell.y and current_cell.x == start_cell.x):
        next_step_cell = [
            neighbor
            for neighbor in maze.get_adjacent_reachable_cells(current_cell)
            if path_lengths[neighbor.y][neighbor.x] == path_lengths[current_cell.y][current_cell.x] - 1
        ][0]

        # Once we've found a suitable neighbor, add it to the result.
        path.append(next_step_cell)
        current_cell = next_step_cell

    return path


class Cell:

    def __init__(self, y, x, walls):
        self.y = y
        self.x = x
        self.walls = walls

    def has_wall(self, index):
        return self.walls[index]

    def has_all_walls(self):
        return self.walls.count(True) == len(self.walls)

    def break_wall(self, index):
        self.walls[index] = False

    def __str__(self):
        return "x = %d, y = %d" % (self.x, self.y)


class Maze:
    steps_to_reach_neighbors = [
        # y increment, x increment
        (-1, 0),  # North
        (0, 1),   # East
        (1, 0),   # South
        (0, -1)   # West
    ]

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.cells = [
            [Cell(y, x, [True, True, True, True]) for x in range(0, width)]
            for y in range(0, height)
        ]

    def get_cell_by_coordinate(self, y, x):
        return self.cells[y][x]

    def break_wall_between_cells(self, cell1, cell2):
        y_diff = cell1.y - cell2.y
        x_diff = cell1.x - cell2.x

        # Each cell maintains its own list of walls, so we need to break them symmetrically.
        # E.g., if we break the southern wall of cell 1, we also need to break the northern wall of cell 2.
        cell1_neighbor_index = self.steps_to_reach_neighbors.index((-y_diff, -x_diff))
        cell2_neighbor_index = self.steps_to_reach_neighbors.index((y_diff, x_diff))
        cell1.break_wall(cell1_neighbor_index)
        cell2.break_wall(cell2_neighbor_index)

    def exists_wall_between_cells(self, cell1, cell2):
        y_diff = cell1.y - cell2.y
        x_diff = cell1.x - cell2.x
        wall_index = self.steps_to_reach_neighbors.index((y_diff, x_diff))
        return cell2.has_wall(wall_index)

    def get_adjacent_cells(self, cell):
        return list([
            self.get_cell_by_coordinate(cell.y + step[0], cell.x + step[1])
            for step in self.steps_to_reach_neighbors
            if 0 <= cell.y + step[0] < self.height and 0 <= cell.x + step[1] < self.width
        ])

    def get_adjacent_reachable_cells(self, cell):
        return [
            # Return the N, E, S, W neighbors...
            neighbor
            for neighbor in self.get_adjacent_cells(cell)
            # ...as long as there's no wall between us and the neighbor.
            if not self.exists_wall_between_cells(cell, neighbor)
        ]


class UI:
    color_window_background = "#D0D0D0"
    color_cell_background = "#FFFFFF"
    color_solved_cell_background = "#CCE5FF"
    color_cell_text = "#000000"
    color_wall = "#000000"
    color_trace = "#800000"

    def __init__(self, maze_height, maze_width, maze_cell_size, animation_delay):
        self.maze_height = maze_height
        self.maze_width = maze_width
        self.maze_cell_size = maze_cell_size
        self.animation_delay = animation_delay

        self.window = None
        self.button_frame = None
        self.canvas_frame = None
        self.canvas = None
        self.go_button = None

        self.create_window()
        self.create_widgets()

    def create_window(self):
        self.window = Tk()
        self.window.title("Maze Algorithms")
        self.window.configure(background=self.color_window_background)
        self.window.resizable(0, 0)

    def create_widgets(self):
        self.create_buttons()
        self.create_canvas()

    def create_buttons(self):
        self.button_frame = Frame(self.window, padx=10, pady=10, background=self.color_window_background)
        self.button_frame.pack()
        self.go_button = Button(self.button_frame, text="Go!")
        self.go_button.configure(highlightbackground=self.color_window_background)
        self.go_button.pack()

    def create_canvas(self):
        self.canvas_frame = Frame(self.window, padx=30, pady=30, borderwidth=0)
        self.canvas_frame.configure(background=self.color_window_background)
        self.canvas_frame.pack()
        self.canvas = Canvas(
            self.canvas_frame,
            width=self.maze_width * self.maze_cell_size + 2,
            height=self.maze_height * self.maze_cell_size + 2,
            background=self.color_window_background,
            borderwidth=0,
            highlightthickness=0
        )
        self.canvas.pack()

    def set_action_for_go_button(self, action):
        def wrapped_action():
            # Clear the canvas.
            self.canvas.delete("all")

            # Block the button until its action is completed.
            self.go_button.configure(state=DISABLED)
            action()
            self.go_button.configure(state=NORMAL)

        self.go_button.configure(command=wrapped_action)

    def draw_maze(self, maze):
        for y in range(0, maze.height):
            for x in range(0, maze.width):
                cell = maze.get_cell_by_coordinate(y, x)
                self.draw_cell(cell)

    def draw_cell(self, cell, color=color_cell_background, text=None):
        cell_upper_left_x = cell.x * self.maze_cell_size + 1
        cell_upper_left_y = cell.y * self.maze_cell_size + 1

        # Paint cell background.
        self.canvas.create_rectangle(
            cell_upper_left_x,
            cell_upper_left_y,
            cell_upper_left_x + self.maze_cell_size,
            cell_upper_left_y + self.maze_cell_size,
            width=0,
            fill=color
        )

        # Paint text, if specified.
        if text is not None:
            self.canvas.create_text(
                cell_upper_left_x + self.maze_cell_size / 2,
                cell_upper_left_y + self.maze_cell_size / 2,
                font=("", 8),
                fill=self.color_cell_text,
                text=str(text)
            )

        # Paint walls.
        wall_line_templates = [
            # x1, y1, x2, y2
            (0, 0, 1, 0),  # Northern
            (1, 0, 1, 1),  # Eastern
            (0, 1, 1, 1),  # Southern
            (0, 0, 0, 1)   # Western
        ]

        for wall_index in range(0, len(cell.walls)):
            if cell.has_wall(wall_index):
                wall_template = wall_line_templates[wall_index]
                self.canvas.create_line(
                    cell_upper_left_x + wall_template[0] * self.maze_cell_size,
                    cell_upper_left_y + wall_template[1] * self.maze_cell_size,
                    cell_upper_left_x + wall_template[2] * self.maze_cell_size,
                    cell_upper_left_y + wall_template[3] * self.maze_cell_size,
                    fill=self.color_wall
                )

    def draw_trace(self, cell, previous_cell):
        current_cell_center_x = cell.x * self.maze_cell_size + self.maze_cell_size / 2
        current_cell_center_y = cell.y * self.maze_cell_size + self.maze_cell_size / 2
        previous_cell_center_x = previous_cell.x * self.maze_cell_size + self.maze_cell_size / 2
        previous_cell_center_y = previous_cell.y * self.maze_cell_size + self.maze_cell_size / 2

        self.canvas.create_line(
            previous_cell_center_x,
            previous_cell_center_y,
            current_cell_center_x,
            current_cell_center_y,
            width=3,
            fill=self.color_trace
        )

    def do_animation_delay(self):
        time.sleep(self.animation_delay)
        self.canvas.update()

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    main()
