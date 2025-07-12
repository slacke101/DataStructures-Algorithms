import tkinter as tk
import ttkbootstrap as ttk
import time
import random
from ttkbootstrap.constants import *


class SortingVisualizer:
    # Color and UI constants
    BAR_COLORS = ["#4F8EF7", "#7B5FEA", "#A259F7", "#F246F5"]  # Blue to purple gradient
    SWAP_COLOR = "#E94F37"  # Red for swaps
    COMPARE_COLOR = "#F7B32B"  # Yellow for comparisons
    COMPLETE_COLOR = "#4CAF50"  # Green for completion
    BG_COLOR = "#F4F4F4"  # Background color
    BAR_WIDTH = 32
    PADDING = 40
    ARRAY = [12, 8, 14, 19, 2, 7, 1, 3, 17, 4]  # Default array to sort
    FONT = ("Segoe UI", 11)
    BUTTON_FONT = ("Segoe UI", 10, "bold")

    def __init__(self, master):
        """
        Initialize the visualizer, set up UI, and draw the initial bars.
        """
        self.master = master
        self.master.configure(bg=self.BG_COLOR)
        self.data = list(self.ARRAY)  # Copy of the array to sort
        self.n = len(self.data)
        self.i = 0  # Outer loop index for bubble sort
        self.j = 0  # Inner loop index for bubble sort
        self.sorting = False  # Sorting state flag
        self.after_id = None  # Tkinter after() callback id
        self.step_count = 0  # Number of steps taken
        self.last_action = ""  # Last action description
        self.completion_pulse = 0  # Animation pulse for completion
        self.pulse_direction = 1  # Direction of pulse
        self.animation_speed = 400  # Animation speed in milliseconds
        self.setup_ui()
        self.draw_bars()

    def setup_ui(self):
        """
        Set up the UI: buttons, labels, and canvas for drawing bars.
        """
        # Main control frame
        control_frame = ttk.Frame(self.master)
        control_frame.pack(fill=tk.X, padx=10, pady=10)

        # Button frame
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))

        # Start button
        self.start_btn = ttk.Button(
            button_frame,
            text="Start",
            command=self.start_sort,
            style="primary.TButton",
            width=10,
        )
        self.start_btn.pack(side=tk.LEFT, padx=8)

        # Reset button
        self.reset_btn = ttk.Button(
            button_frame,
            text="Reset",
            command=self.reset,
            style="danger.TButton",
            width=10,
        )
        self.reset_btn.pack(side=tk.LEFT, padx=8)

        # Generate Random Array button
        self.random_btn = ttk.Button(
            button_frame,
            text="Random Array",
            command=self.generate_random_array,
            style="success.TButton",
            width=12,
        )
        self.random_btn.pack(side=tk.LEFT, padx=8)

        # Settings frame
        settings_frame = ttk.Frame(control_frame)
        settings_frame.pack(fill=tk.X, pady=5)

        # Array size control
        size_frame = ttk.Frame(settings_frame)
        size_frame.pack(side=tk.LEFT, padx=(0, 20))

        ttk.Label(size_frame, text="Array Size:", font=("Segoe UI", 9)).pack(
            side=tk.LEFT
        )
        self.size_slider = ttk.Scale(
            size_frame,
            from_=5,
            to=30,
            orient="horizontal",
            value=len(self.ARRAY),
            command=self.on_size_change,
            length=150,
        )
        self.size_slider.pack(side=tk.LEFT, padx=(5, 0))
        self.size_label = ttk.Label(
            size_frame, text=str(len(self.ARRAY)), font=("Segoe UI", 9)
        )
        self.size_label.pack(side=tk.LEFT, padx=(5, 0))

        # Speed control
        speed_frame = ttk.Frame(settings_frame)
        speed_frame.pack(side=tk.LEFT, padx=(0, 20))

        ttk.Label(speed_frame, text="Speed:", font=("Segoe UI", 9)).pack(side=tk.LEFT)
        self.speed_slider = ttk.Scale(
            speed_frame,
            from_=50,
            to=1000,
            orient="horizontal",
            value=400,
            command=self.on_speed_change,
            length=150,
        )
        self.speed_slider.pack(side=tk.LEFT, padx=(5, 0))
        self.speed_label = ttk.Label(speed_frame, text="400ms", font=("Segoe UI", 9))
        self.speed_label.pack(side=tk.LEFT, padx=(5, 0))

        # Complexity label
        self.complexity_label = ttk.Label(
            self.master,
            text="Bubble Sort: O(n²)",
            style="info.TLabel",
            font=("Segoe UI", 13, "bold"),
        )
        self.complexity_label.pack(pady=(0, 10))

        # Canvas for drawing bars
        self.canvas = tk.Canvas(
            self.master, height=350, bg="white", highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Info label for step-by-step action
        self.info_label = ttk.Label(
            self.master, text="", style="secondary.TLabel", font=self.FONT
        )
        self.info_label.pack(pady=(0, 10))

    def on_size_change(self, value):
        """Handle array size slider changes"""
        if not self.sorting:
            new_size = int(value)
            self.size_label.config(text=str(new_size))
            self.generate_array_of_size(new_size)
            self.draw_bars()

    def on_speed_change(self, value):
        """Handle speed slider changes"""
        self.animation_speed = int(value)
        self.speed_label.config(text=f"{self.animation_speed}ms")

    def generate_random_array(self):
        """Generate a new random array"""
        if not self.sorting:
            size = int(self.size_slider.get())
            self.generate_array_of_size(size)
            self.draw_bars()

    def generate_array_of_size(self, size):
        """Generate a random array of specified size"""
        self.data = [random.randint(1, 20) for _ in range(size)]
        self.n = len(self.data)
        self.i = 0
        self.j = 0
        self.step_count = 0
        self.last_action = ""

    def draw_gradient_bg(self):
        """
        Draw a vertical gradient background on the canvas for visual appeal.
        """
        w = int(self.canvas.winfo_width()) or (
            self.n * self.BAR_WIDTH + 2 * self.PADDING
        )
        h = int(self.canvas.winfo_height()) or 350
        for i in range(h):
            r1, g1, b1 = 244, 244, 244  # #F4F4F4
            r2, g2, b2 = 194, 233, 251  # #C2E9FB
            r = int(r1 + (r2 - r1) * i / h)
            g = int(g1 + (g2 - g1) * i / h)
            b = int(b1 + (b2 - b1) * i / h)
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.canvas.create_line(0, i, w, i, fill=color)

    def draw_bars(self, highlight=None, complete=False):
        """
        Draw the array as bars on the canvas, highlighting comparisons/swaps.
        Args:
            highlight: dict with keys 'swap' (bool), and indices to highlight
            complete: if True, pulse bars green for completion
        """
        self.canvas.delete("all")
        self.draw_gradient_bg()
        w = int(self.canvas.winfo_width()) or (
            self.n * self.BAR_WIDTH + 2 * self.PADDING
        )
        h = int(self.canvas.winfo_height()) or 350
        bar_width = max(self.BAR_WIDTH, (w - 2 * self.PADDING) // max(1, self.n))
        max_val = max(self.data) if self.data else 1
        axis_y = h - 20
        # Draw x-axis
        self.canvas.create_line(
            self.PADDING - 10,
            axis_y,
            w - self.PADDING + 10,
            axis_y,
            fill="#888",
            width=2,
        )
        for idx, val in enumerate(self.data):
            x0 = self.PADDING + idx * bar_width
            x1 = x0 + bar_width - 2
            y1 = axis_y
            y0 = y1 - int((val / max_val) * (h - 60))
            # Gradient color for bars
            color = self.BAR_COLORS[idx % len(self.BAR_COLORS)]
            if highlight and idx in highlight:
                color = self.SWAP_COLOR if highlight["swap"] else self.COMPARE_COLOR
            if complete:
                # Pulse green on completion
                pulse = 180 + int(60 * abs(self.completion_pulse))
                color = f"#4C{pulse:02X}50"  # Vary green channel
            # Draw shadow
            self.canvas.create_rectangle(
                x0 + 3, y0 + 8, x1 + 3, y1 + 8, fill="#bbb", outline=""
            )
            # Draw rounded bar (simulate with two ovals and a rectangle)
            self.canvas.create_rectangle(
                x0, y0 + 8, x1, y1, fill=color, outline="", width=0
            )
            self.canvas.create_oval(x0, y0, x1, y0 + 16, fill=color, outline="")
            self.canvas.create_oval(x0, y1 - 16, x1, y1, fill=color, outline="")
            self.canvas.create_text(
                x0 + bar_width // 2,
                y1 + 12,
                text=str(val),
                font=("Segoe UI", 9, "bold"),
                fill="#333",
            )
        self.master.update_idletasks()
        self.info_label.config(text=self.last_action)

    def start_sort(self):
        """
        Start the bubble sort animation. Disables buttons during sorting.
        """
        if self.sorting:
            return
        self.sorting = True
        self.start_btn.configure(state="disabled")
        self.reset_btn.configure(state="disabled")
        self.random_btn.configure(state="disabled")
        self.size_slider.configure(state="disabled")
        self.speed_slider.configure(state="disabled")
        self.i = 0
        self.j = 0
        self.step_count = 0
        self.last_action = ""
        self.bubble_step()

    def bubble_step(self):
        """
        Perform one step of the bubble sort and update the visualization.
        Uses self.i and self.j to track progress.
        """
        if self.i < self.n - 1:
            if self.j < self.n - self.i - 1:
                self.step_count += 1
                highlight = {"swap": False, self.j: True, self.j + 1: True}
                action = f"Step {self.step_count}: Comparing index {self.j} ({self.data[self.j]}) and {self.j + 1} ({self.data[self.j + 1]})"
                if self.data[self.j] > self.data[self.j + 1]:
                    self.data[self.j], self.data[self.j + 1] = (
                        self.data[self.j + 1],
                        self.data[self.j],
                    )
                    highlight = {"swap": True, self.j: True, self.j + 1: True}
                    action = f"Step {self.step_count}: Swapped index {self.j} and {self.j + 1} -> {self.data[self.j]} <-> {self.data[self.j + 1]}"
                self.last_action = action
                self.draw_bars(highlight)
                self.j += 1
                self.after_id = self.master.after(
                    self.animation_speed, self.bubble_step
                )
            else:
                self.j = 0
                self.i += 1
                self.after_id = self.master.after(
                    self.animation_speed, self.bubble_step
                )
        else:
            self.last_action = f"Done! Sorted array: {self.data}"
            self.completion_pulse = 0
            self.pulse_direction = 1
            self.animate_completion()
            self.sorting = False
            self.start_btn.configure(state="normal")
            self.reset_btn.configure(state="normal")
            self.random_btn.configure(state="normal")
            self.size_slider.configure(state="normal")
            self.speed_slider.configure(state="normal")

    def animate_completion(self):
        """
        Animate the bars pulsing green to indicate completion.
        """
        self.completion_pulse += 0.08 * self.pulse_direction
        if self.completion_pulse > 1:
            self.completion_pulse = 1
            self.pulse_direction = -1
        elif self.completion_pulse < 0:
            self.completion_pulse = 0
            return  # End pulse
        self.draw_bars(complete=True)
        self.after_id = self.master.after(self.animation_speed, self.animate_completion)

    def reset(self):
        """
        Reset the array and UI to the initial state. Cancels any running animation.
        """
        if self.after_id:
            self.master.after_cancel(self.after_id)
            self.after_id = None
        self.data = list(self.ARRAY)
        self.i = 0
        self.j = 0
        self.sorting = False
        self.step_count = 0
        self.last_action = ""
        self.completion_pulse = 0
        self.pulse_direction = 1
        self.start_btn.configure(state="normal")
        self.reset_btn.configure(state="normal")
        self.random_btn.configure(state="normal")
        self.size_slider.configure(state="normal")
        self.speed_slider.configure(state="normal")
        self.draw_bars()
