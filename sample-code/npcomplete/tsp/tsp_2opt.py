from Tkinter import *

import random
import time
import collections

Point = collections.namedtuple(typename='Point', field_names=['x', 'y'])


def main():
    height = 600
    width = 300
    animation_delay = 0.005
    points = []

    def generate_and_draw_points():
        global points
        count = ui.get_point_count_spinbox_value()
        points = generate_points(ui.width, ui.height, count)
        ui.draw_points(points)

    def begin_solving_2opt():
        def on_segments_optimized(worse_segments, better_segments, new_tour):
            for segment in worse_segments:
                ui.draw_segment(segment[0], segment[1], ui.color_worse_segment)
            ui.do_animation_delay()

            for segment in better_segments:
                ui.draw_segment(segment[0], segment[1], ui.color_better_segment)
            ui.do_animation_delay()

            ui.draw_tour(new_tour)
            ui.do_animation_delay()

        global points
        solve_2opt(points, on_segments_optimized)

    ui = UI(height, width, animation_delay)
    ui.set_action_for_generate_button(generate_and_draw_points)
    ui.set_action_for_solve_2opt_button(begin_solving_2opt)
    ui.run()


def generate_points(width, height, count):
    padding = 5
    return [
        Point(
            x=random.randint(padding, width - padding),
            y=random.randint(padding, height - padding)
        )
        for i in range(count)
    ]


def distance(point1, point2):
    return ((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2) ** 0.5


def slice_tour(tour, start_point_index, end_point_index):
    result = []

    current_point_index = start_point_index
    while current_point_index != end_point_index:
        result.append(tour[current_point_index])
        current_point_index = (current_point_index + 1) % len(tour)

    result.append(tour[end_point_index])
    return result


def solve_2opt(points, segments_optimized_callback):
    # Our first approximation is just a random tour.
    current_tour = points[:]
    segments_optimized_callback(worse_segments=[], better_segments=[], new_tour=current_tour)

    # Starting from that, we'll look for crossing segments in our path, and optimize them like this:
    #
    #   ------ point1   point2 ------       ------ point1 --- point2 ------
    #                \ /
    #                 X                ==>
    #                / \
    #   --- neighbor2   neighbor1 ---       --- neighbor2 --- neighbor1 ---
    #
    better_tour_found = True
    while better_tour_found:
        better_tour = None
        better_tour_found = False

        # Looking up all possible pairs of (point1, point2) and checking if there's an optimization possible:
        for (i, point1) in enumerate(current_tour):
            for (j, point2) in enumerate(current_tour):

                # The % operator takes care of the situation when i = len(current_tour) - 1 and i_neighbor = 0.
                i_neighbor = (i + 1) % len(current_tour)
                j_neighbor = (j + 1) % len(current_tour)
                neighbor1 = current_tour[i_neighbor]
                neighbor2 = current_tour[j_neighbor]

                # Making sure that all of our 4 points are distinct.
                if i != j and i_neighbor != j_neighbor and i_neighbor != j and j_neighbor != i:
                    current_distance = distance(point1, neighbor1) + distance(point2, neighbor2)
                    alternative_distance = distance(point1, point2) + distance(neighbor1, neighbor2)

                    # If "direct" path is better than "crossing" path, building the new tour and remembering it.
                    if alternative_distance < current_distance:
                        better_tour = list(reversed(slice_tour(current_tour, i_neighbor, j))) + slice_tour(current_tour, j_neighbor, i)
                        better_tour_found = True
                        segments_optimized_callback(
                            worse_segments=[[point1, neighbor1], [point2, neighbor2]],
                            better_segments=[[point1, point2], [neighbor1, neighbor2]],
                            new_tour=better_tour
                        )
                        break

            if better_tour_found:
                break

        if better_tour_found:
            current_tour = better_tour


class UI:
    color_window_background = "#D0D0D0"
    color_canvas_border = "#000000"
    color_canvas_background = "#FFFFFF"
    color_point = "#000000"
    color_segment = "#000000"
    color_worse_segment = "#D80000"
    color_better_segment = "#00CC00"

    point_radius = 3
    segment_width = 3

    default_point_count = 10
    min_point_count = 4
    max_point_count = 200

    def __init__(self, width, height, animation_delay):
        self.width = width
        self.height = height
        self.animation_delay = animation_delay

        self.window = None
        self.button_frame = None
        self.canvas_frame = None
        self.canvas = None

        self.point_count_label = None
        self.point_count_spinbox = None
        self.point_count_var = None
        self.generate_button = None
        self.solve_2opt_button = None

        self.create_window()
        self.create_widgets()

    def create_window(self):
        self.window = Tk()
        self.window.title("Traveling Salesman Problem (TSP)")
        self.window.configure(background=self.color_window_background)
        self.window.resizable(0, 0)

    def create_widgets(self):
        self.create_controls()
        self.create_canvas()

    def create_controls(self):
        self.button_frame = Frame(self.window, padx=10, pady=10, background=self.color_window_background)
        self.button_frame.pack()

        self.point_count_label = Label(self.button_frame, text="Number of Points:")
        self.point_count_label.configure(background=self.color_window_background)
        self.point_count_label.pack(padx=5, side=LEFT)

        self.point_count_var = IntVar(self.window)
        self.point_count_var.set(self.default_point_count)

        self.point_count_spinbox = Spinbox(self.button_frame,from_=self.min_point_count, to=self.max_point_count, width=20, textvariable=self.point_count_var)
        self.point_count_spinbox.configure(width=5)
        self.point_count_spinbox.pack(side=LEFT)

        self.generate_button = Button(self.button_frame, text="Generate")
        self.generate_button.configure(highlightbackground=self.color_window_background)
        self.generate_button.pack(padx=10, side=LEFT)

        self.solve_2opt_button = Button(self.button_frame, text="Solve: 2-OPT Heuristic")
        self.solve_2opt_button.configure(highlightbackground=self.color_window_background, state=DISABLED)
        self.solve_2opt_button.pack(padx=10, side=LEFT)

    def create_canvas(self):
        self.canvas_frame = Frame(self.window, padx=30, pady=30, borderwidth=0)
        self.canvas_frame.configure(background=self.color_window_background)
        self.canvas_frame.pack()
        self.canvas = Canvas(
            self.canvas_frame,
            width=self.width,
            height=self.height,
            background=self.color_canvas_background,
            borderwidth=1,
            highlightbackground=self.color_canvas_border,
            highlightcolor=self.color_canvas_border,
            highlightthickness=1
        )
        self.canvas.pack()

    def get_point_count_spinbox_value(self):
        try:
            point_count = int(self.point_count_spinbox.get())
        except:
            point_count = self.default_point_count

        point_count = max(point_count, self.min_point_count)
        point_count = min(point_count, self.max_point_count)
        self.point_count_var.set(str(point_count))
        return point_count

    def set_enabled_state_for_buttons(self, is_enabled):
        buttons = [self.generate_button, self.solve_2opt_button]
        for button in buttons:
            button.configure(state=NORMAL if is_enabled else DISABLED)

    def set_action_for_generate_button(self, action):
        def wrapped_action():
            # Clear the canvas.
            self.canvas.delete("all")

            # Block the button until its action is completed.
            self.set_enabled_state_for_buttons(False)
            action()
            self.set_enabled_state_for_buttons(True)

        self.generate_button.configure(command=wrapped_action)

    def set_action_for_solve_2opt_button(self, action):
        def wrapped_action():
            # Block the button until its action is completed.
            self.set_enabled_state_for_buttons(False)
            action()
            self.set_enabled_state_for_buttons(True)

        self.solve_2opt_button.configure(command=wrapped_action)

    def draw_points(self, points):
        for point in points:
            self.draw_point(point)

    def draw_point(self, point):
        self.canvas.create_oval(
            point.x - self.point_radius,
            point.y - self.point_radius,
            point.x + self.point_radius,
            point.y + self.point_radius,
            fill=self.color_point,
            width=1
        )

    def draw_tour(self, tour):
        self.canvas.delete("all")
        self.draw_points(tour)
        for i in range(0, len(tour)):
            self.draw_segment(tour[i], tour[(i + 1) % len(tour)], self.color_segment)

    def draw_segment(self, point1, point2, color):
        self.canvas.create_line(
            point1.x,
            point1.y,
            point2.x,
            point2.y,
            width=self.segment_width,
            fill=color
        )
        self.draw_point(point1)
        self.draw_point(point2)

    def do_animation_delay(self):
        time.sleep(self.animation_delay)
        self.canvas.update()

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    main()
