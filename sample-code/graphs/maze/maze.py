import random
import time
from Tkinter import *


def main():
    height = 25
    width = 40

    maze_cell_size = 25
    animation_delay = 0.005

    ui = UI(height, width, maze_cell_size, animation_delay)

    def begin_simulation():
        def on_cell_changed(cell, previous_cell):
            ui.draw_cell(cell, ui.color_cell_background)
            if previous_cell is not None:
                ui.draw_cell(previous_cell, ui.color_cell_background)
            ui.do_animation_delay()

        def on_cell_solved(cell, label=None):
            ui.draw_cell(cell, ui.color_solved_cell_background, label)
            ui.do_animation_delay()

        def on_trace_next_step(cell, previous_cell):
            ui.draw_trace(cell, previous_cell)
            ui.do_animation_delay()

        # Generate a perfect maze (the one that has a unique path between every two cells).
        maze = generate_maze(height, width, on_cell_changed)

        # Make the maze more interesting by removing random walls, thus producing alternative paths.
        remove_random_walls(maze, height * width / 4)

        ui.draw_maze(maze)

        # Calculate shortest paths to every cell and backtrace the path between start and end.
        path_lengths = solve_maze(maze, on_cell_solved)
        trace_exit_path(maze, path_lengths, on_trace_next_step)

    # Bind the button to the maze generation action and run the window loop.
    ui.set_generate_button_action(begin_simulation)
    ui.mainloop()


def generate_maze(height, width, cell_changed_callback=None):
    maze = Maze(height, width)
    start_cell = maze.get_cell_by_coordinate(0, 0)

    # Just doing the typical DFS: putting the start cell in the stack,
    # but for this task we'll be also storing the cell we came from.
    # So we'll write PAIRS of items to the stack, and read pairs as well.
    stack = [(start_cell, None)]
    visited = [[False for x in range(0, width)] for y in range(0, height)]

    while len(stack) > 0:
        # Retrieve another pair of items from the stack.
        current_cell, previous_cell = stack.pop()

        # Break a wall between the current cell and the previous cell.
        if previous_cell is not None and not visited[current_cell.y][current_cell.x]:
            maze.break_wall_between_cells(previous_cell, current_cell)

            # Notify the UI that we've created a new cell.
            if cell_changed_callback is not None:
                cell_changed_callback(current_cell, previous_cell)

        # Mark this cell so we won't visit it anymore.
        visited[current_cell.y][current_cell.x] = True

        # Get all neighbors that have all 4 walls intact.
        neighbors = maze.get_adjacent_cells(current_cell)
        filtered_neighbors = list([neighbor
                                   for neighbor in neighbors
                                   if not visited[neighbor.y][neighbor.x] and neighbor.has_all_walls()])

        # Shuffle the neighbors so we'll visit them in random order.
        # That will make our maze much more interesting.
        random.shuffle(filtered_neighbors)
        stack.extend([(neighbor, current_cell) for neighbor in filtered_neighbors])

    return maze


def solve_maze(maze, new_cell_callback=None):
    # Just doing the usual BFS, but, in addition to the cell itself,
    # also store the length of the path from start to {x, y} in the queue.
    # Because it's BFS and the graph is not weighted, the path length will
    # also be the MINIMUM path length. Obviously, it's 1 for the start cell.
    queue = [(maze.cells[0][0], 1)]

    visited = [[False for x in range(0, maze.width)] for y in range(0, maze.height)]
    path_lengths = [[None for x in range(0, maze.width)] for y in range(0, maze.height)]

    while len(queue) > 0:
        # Fetch a new {cell, path_length} pair from the queue.
        current_cell, moves = queue.pop(0)

        if visited[current_cell.y][current_cell.x]:
            continue

        # Notify the UI that we've visited a new cell.
        if new_cell_callback is not None:
            new_cell_callback(current_cell, moves)

        visited[current_cell.y][current_cell.x] = True
        path_lengths[current_cell.y][current_cell.x] = moves

        # Discovering the unvisited neighbors that are reachable from the current_cell
        # (the ones that don't have walls between them and our cell).
        neighbors = maze.get_adjacent_reachable_cells(current_cell)

        # Every neighbor will have a (moves + 1) minimum path length.
        queue.extend([(neighbor, moves + 1) for neighbor in neighbors])

    return path_lengths


def remove_random_walls(maze, wall_count):
    removed_count = 0
    while removed_count < wall_count:
        x = random.randint(1, maze.width - 2)
        y = random.randint(1, maze.height - 2)

        # If there's a horizontal or vertical wall that spans 3 consecutive cells,
        # we're safe to remove the middle wall without introducing any open areas.
        cell = maze.cells[y][x]
        if cell.has_wall(1) and maze.cells[y][x - 1].has_wall(1) and maze.cells[y][x + 1].has_wall(1):
            maze.break_wall_between_cells(cell, maze.cells[y + 1][x])
            removed_count += 1
        if cell.has_wall(0) and maze.cells[y - 1][x].has_wall(0) and maze.cells[y + 1][x].has_wall(1):
            maze.break_wall_between_cells(cell, maze.cells[y][x + 1])
            removed_count += 1


def trace_exit_path(maze, path_lengths, new_step_callback=None):
    # Start from the bottom right cell.
    y = maze.height - 1
    x = maze.width - 1

    moves = path_lengths[y][x]
    current_cell = maze.cells[y][x]

    # Move to a neighbor cell that has a path length of (moves - 1) until we reach the start cell.
    while moves != 1:
        next_step_cell = [neighbor for neighbor in maze.get_adjacent_reachable_cells(current_cell)
                          if path_lengths[neighbor.y][neighbor.x] == moves - 1][0]

        # Notify the UI that we've made a new step.
        if new_step_callback is not None:
            new_step_callback(next_step_cell, current_cell)

        current_cell = next_step_cell
        moves -= 1


class Cell:
    walls = []

    def __init__(self, y, x, walls):
        self.y = y
        self.x = x
        self.walls = walls

    def has_wall(self, index):
        return self.walls[index]

    def break_wall(self, index):
        self.walls[index] = False

    def has_all_walls(self):
        return self.walls.count(True) == len(self.walls)

    def __str__(self):
        return "x = %d  y = %d" % (self.x, self.y)


class Maze:
    # The (y, x) steps we need to make to reach the northern,
    # eastern, southern and western neighbors, respectively.
    neighbor_increments = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.cells = [[Cell(y, x, [True, True, True, True])
                       for x in range(0, width)]
                      for y in range(0, height)]

    def get_cell_by_coordinate(self, y, x):
        return self.cells[y][x]

    def get_adjacent_cells(self, cell):
        # Return the N, E, S, W neighbors, as long as we don't cross the maze boundaries.
        return list([self.get_cell_by_coordinate(cell.y + increment[0], cell.x + increment[1])
                     for increment in self.neighbor_increments
                     if 0 <= cell.y + increment[0] < self.height and 0 <= cell.x + increment[1] < self.width])

    def exists_path_between_cells(self, cell1, cell2):
        y_diff = cell1.y - cell2.y
        x_diff = cell1.x - cell2.x
        return not cell2.has_wall(self.neighbor_increments.index((y_diff, x_diff)))

    def get_adjacent_reachable_cells(self, cell):
        # Return the N, E, S, W neighbors, as long as there's no wall and we don't cross the maze boundaries.
        return [self.get_cell_by_coordinate(cell.y + increment[0], cell.x + increment[1])
                for increment in self.neighbor_increments
                if 0 <= cell.y + increment[0] < self.height and 0 <= cell.x + increment[1] < self.width
                   and self.exists_path_between_cells(cell, self.cells[cell.y + increment[0]][cell.x + increment[1]])]

    def break_wall_between_cells(self, cell1, cell2):
        y_diff = cell1.y - cell2.y
        x_diff = cell1.x - cell2.x

        # We need to break walls symmetrically, e.g. northern wall for one cell, southern for the other.
        cell1.break_wall(self.neighbor_increments.index((-y_diff, -x_diff)))
        cell2.break_wall(self.neighbor_increments.index((y_diff, x_diff)))


class UI:
    color_window_background = "#D0D0D0"
    color_cell_background = "#FFFFFF"
    color_path_length_label = "#000000"
    color_solved_cell_background = "#CCE5FF"
    color_wall = "#000000"
    color_trace = "#800000"

    def __init__(self, maze_height, maze_width, maze_cell_size, animation_delay):
        self.maze_height = maze_height
        self.maze_width = maze_width
        self.maze_cell_size = maze_cell_size
        self.animation_delay = animation_delay

        self.window = Tk()
        self.window.title("Maze Algorithms")
        self.window.configure(background=self.color_window_background)
        self.window.resizable(0, 0)

        self.create_widgets()

    def create_widgets(self):
        self.button_frame = Frame(self.window, padx=10, pady=10, background=self.color_window_background)
        self.button_frame.pack()
        self.generate_button = Button(self.button_frame, text="Generate and Solve")
        self.generate_button.pack()
        self.create_canvas()

    def create_canvas(self):
        self.canvas_frame = Frame(self.window, padx=30, pady=30, borderwidth=0)
        self.canvas_frame.configure(background=self.color_window_background)
        self.canvas_frame.pack()
        self.canvas = Canvas(self.canvas_frame,
                             width=self.maze_width * self.maze_cell_size + 2,
                             height=self.maze_height * self.maze_cell_size + 2,
                             background=self.color_window_background,
                             borderwidth=0,
                             highlightthickness=0)
        self.canvas.pack()

    def set_generate_button_action(self, action):
        def button_action():
            self.canvas_frame.destroy()
            self.create_canvas()

            self.generate_button.configure(state=DISABLED)
            action()
            self.generate_button.configure(state=NORMAL)

        self.generate_button.configure(command=button_action)

    def draw_maze(self, maze):
        for y in range(0, maze.height):
            for x in range(0, maze.width):
                cell = maze.get_cell_by_coordinate(y, x)
                self.draw_cell(cell, self.color_cell_background)

    def draw_cell(self, cell, color, label=None):
        cell_upper_left_x = cell.x * self.maze_cell_size + 1
        cell_upper_left_y = cell.y * self.maze_cell_size + 1

        self.canvas.create_rectangle(cell_upper_left_x,
                                     cell_upper_left_y,
                                     cell_upper_left_x + self.maze_cell_size,
                                     cell_upper_left_y + self.maze_cell_size,
                                     width=0,
                                     fill=color)

        if label is not None:
            self.canvas.create_text(cell_upper_left_x + self.maze_cell_size / 2,
                                    cell_upper_left_y + self.maze_cell_size / 2,
                                    font=("", 8),
                                    fill=self.color_path_length_label,
                                    text=str(label))

        line_templates = [(0, 0, 1, 0),
                          (1, 0, 1, 1),
                          (0, 1, 1, 1),
                          (0, 0, 0, 1)]

        for wall_index in range(0, len(cell.walls)):
            if cell.has_wall(wall_index):
                wall_template = line_templates[wall_index]
                self.canvas.create_line(cell_upper_left_x + wall_template[0] * self.maze_cell_size,
                                        cell_upper_left_y + wall_template[1] * self.maze_cell_size,
                                        cell_upper_left_x + wall_template[2] * self.maze_cell_size,
                                        cell_upper_left_y + wall_template[3] * self.maze_cell_size,
                                        fill=self.color_wall)

    def draw_trace(self, cell, previous_cell):
        current_cell_center_x = cell.x * self.maze_cell_size + self.maze_cell_size / 2
        current_cell_center_y = cell.y * self.maze_cell_size + self.maze_cell_size / 2
        previous_cell_center_x = previous_cell.x * self.maze_cell_size + self.maze_cell_size / 2
        previous_cell_center_y = previous_cell.y * self.maze_cell_size + self.maze_cell_size / 2

        self.canvas.create_line(previous_cell_center_x,
                                previous_cell_center_y,
                                current_cell_center_x,
                                current_cell_center_y,
                                width=3,
                                fill=self.color_trace)

    def do_animation_delay(self):
        time.sleep(self.animation_delay)
        self.canvas.update()

    def mainloop(self):
        mainloop()


if __name__ == "__main__":
    main()
