import tkinter as tk
import ttkbootstrap as ttk
import random
import time
import inspect  # For retrieving source code of algorithms
import types  # Added to inspect generator types for DS operations
import math  # Added for math.log2
from ttkbootstrap.constants import *
from algorithms.sorting import SORTING_ALGORITHMS, ALGORITHM_INFO
from algorithms.data_structures import DATA_STRUCTURES, DATA_STRUCTURE_INFO


class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tipwindow or not self.text:
            return
        x, y, _, cy = (
            self.widget.bbox("insert") if hasattr(self.widget, "bbox") else (0, 0, 0, 0)
        )
        x = x + self.widget.winfo_rootx() + 30
        y = y + cy + self.widget.winfo_rooty() + 20
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            tw,
            text=self.text,
            justify=tk.LEFT,
            background="#ffffe0",
            relief=tk.SOLID,
            borderwidth=1,
            font=("Segoe UI", 9),
        )
        label.pack(ipadx=6, ipady=2)

    def hide_tip(self, event=None):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()


class DSASimulator:
    """Comprehensive Data Structures & Algorithms Simulator"""

    def __init__(self, master):
        self.master = master
        self.root = master  # Store root for theme updates
        self.master.title("DSA Simulator - Data Structures & Algorithms")
        self.master.geometry("1200x800")

        # State variables
        self.current_mode = "sorting"  # "sorting" or "data_structures"
        self.current_algorithm = "Bubble Sort"
        self.current_data_structure = "Linked List"
        self.data = [12, 8, 14, 19, 2, 7, 1, 3, 17, 4]
        self.data_structure = None
        self.sorting_generator = None
        self.ds_generator = None
        self.sorting = False
        self.animation_speed = 400
        self.step_count = 0
        self.comparisons = 0
        self.swaps = 0
        self.paused = False  # For pause/resume control
        self.after_id = None  # Tkinter after callback handle for dynamic speed control

        # UI setup
        self.setup_ui()
        self.update_info_panel()
        self.update_explanation(
            "Welcome! Select a mode and press Start to begin the visualization."
        )

    def setup_ui(self):
        """Set up the complete UI"""
        # Main container
        main_frame = ttk.Frame(self.master)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Top control panel
        self.setup_control_panel(main_frame)

        # Main content area
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=20)

        # Left panel - Visualization
        self.setup_visualization_panel(content_frame)

        # Right panel - Information and Controls
        self.setup_info_panel(content_frame)

    def setup_control_panel(self, parent):
        """Set up the top control panel"""
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, pady=(0, 20))

        # Theme switcher
        theme_frame = ttk.Frame(control_frame)
        theme_frame.pack(side=tk.LEFT, padx=(0, 20))
        ttk.Label(theme_frame, text="Theme:", font=("Segoe UI", 10, "bold")).pack(
            side=tk.LEFT
        )
        self.theme_var = tk.StringVar(value=self.master.style.theme.name)
        theme_names = [
            "cosmo",
            "flatly",
            "journal",
            "litera",
            "lumen",
            "minty",
            "pulse",
            "sandstone",
            "united",
            "yeti",
            "morph",
            "simplex",
            "cerculean",
            "darkly",
            "solar",
            "superhero",
            "cyborg",
            "vapor",
            "minty",
            "sketchy",
        ]
        theme_combo = ttk.Combobox(
            theme_frame,
            textvariable=self.theme_var,
            values=theme_names,
            state="readonly",
            width=12,
        )
        theme_combo.pack(side=tk.LEFT, padx=(5, 0))
        theme_combo.bind("<<ComboboxSelected>>", self.on_theme_change)

        # Hide theme selector – we’re fixed on the 'superhero' theme for cleaner UI
        theme_frame.pack_forget()

        # Mode selection
        mode_frame = ttk.Frame(control_frame)
        mode_frame.pack(side=tk.LEFT, padx=(0, 20))

        ttk.Label(mode_frame, text="Mode:", font=("Segoe UI", 11, "bold")).pack(
            side=tk.LEFT
        )
        self.mode_var = tk.StringVar(value="sorting")
        mode_combo = ttk.Combobox(
            mode_frame,
            textvariable=self.mode_var,
            values=["Sorting Algorithms", "Data Structures"],
            state="readonly",
            width=20,
        )
        mode_combo.pack(side=tk.LEFT, padx=(5, 0))
        mode_combo.bind("<<ComboboxSelected>>", self.on_mode_change)

        # Algorithm/Data Structure selection
        self.algo_frame = ttk.Frame(control_frame)
        self.algo_frame.pack(side=tk.LEFT, padx=(0, 20))

        ttk.Label(
            self.algo_frame, text="Algorithm:", font=("Segoe UI", 11, "bold")
        ).pack(side=tk.LEFT)
        self.algo_var = tk.StringVar(value="Bubble Sort")
        self.algo_combo = ttk.Combobox(
            self.algo_frame,
            textvariable=self.algo_var,
            values=list(SORTING_ALGORITHMS.keys()),
            state="readonly",
            width=15,
        )
        self.algo_combo.pack(side=tk.LEFT, padx=(5, 0))
        self.algo_combo.bind("<<ComboboxSelected>>", self.on_algorithm_change)

        # Control buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(side=tk.RIGHT)

        self.start_btn = ttk.Button(
            button_frame,
            text="▶️ Start",
            command=self.start_visualization,
            style="primary.TButton",
            width=12,
            bootstyle="rounded",
        )
        self.start_btn.pack(side=tk.LEFT, padx=10)
        ToolTip(self.start_btn, "Start the visualization")

        self.reset_btn = ttk.Button(
            button_frame,
            text="🔄 Reset",
            command=self.reset,
            style="danger.TButton",
            width=12,
            bootstyle="rounded",
        )
        self.reset_btn.pack(side=tk.LEFT, padx=10)
        ToolTip(self.reset_btn, "Reset the visualization")

        self.random_btn = ttk.Button(
            button_frame,
            text="🎲 Random Data",
            command=self.generate_random_data,
            style="success.TButton",
            width=14,
            bootstyle="rounded",
        )
        self.random_btn.pack(side=tk.LEFT, padx=10)
        ToolTip(self.random_btn, "Generate random data for visualization")

        # Add Value entry & button (sorting mode)
        self.add_value_entry = ttk.Entry(button_frame, width=5, font=("Segoe UI", 10))
        self.add_value_entry.pack(side=tk.LEFT, padx=(0, 4))
        self.add_value_entry.insert(0, "5")

        self.add_btn = ttk.Button(
            button_frame,
            text="➕ Add Value",
            command=self.add_value,
            style="success.TButton",
            width=12,
            bootstyle="rounded",
        )
        self.add_btn.pack(side=tk.LEFT, padx=10)
        ToolTip(self.add_btn, "Append a value to the array/bars (sorting mode)")

        # Pause / Resume button
        self.pause_btn = ttk.Button(
            button_frame,
            text="⏸️ Pause",
            command=self.toggle_pause,
            style="warning.TButton",
            width=12,
            bootstyle="rounded",
        )
        self.pause_btn.pack(side=tk.LEFT, padx=10)
        self.pause_btn.configure(state="disabled")
        ToolTip(self.pause_btn, "Pause or resume the visualization")

        # Credits button
        self.credits_btn = ttk.Button(
            button_frame,
            text="⭐ Credits",
            command=self.show_credits,
            style="secondary.TButton",
            width=12,
            bootstyle="rounded",
        )
        self.credits_btn.pack(side=tk.LEFT, padx=10)
        ToolTip(self.credits_btn, "View project credits")

        # Enable keyboard navigation and focus indicators (safe across ttk & tk widgets)
        def _apply_focus_highlight(widget):
            """Safely apply focus/highlight attributes, skipping unsupported ones."""
            try:
                widget.configure(
                    takefocus=True,
                    highlightthickness=2,
                    highlightbackground="#4F8EF7",
                    highlightcolor="#4F8EF7",
                )
            except tk.TclError:
                # Some themed ttk widgets don't support highlight* options
                widget.configure(takefocus=True)

        for _btn in [
            self.start_btn,
            self.reset_btn,
            self.random_btn,
            self.add_btn,
            self.pause_btn,
            self.credits_btn,
        ]:
            _apply_focus_highlight(_btn)

        _apply_focus_highlight(self.add_value_entry)

    # ------------------------------------------------------------------
    # Visualization & Info Panels (restored)
    # ------------------------------------------------------------------

    def setup_visualization_panel(self, parent):
        """Set up the left visualization canvas and status bar"""
        viz_frame = ttk.Frame(parent)
        viz_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))

        # Canvas where bars / nodes will be drawn
        self.canvas = tk.Canvas(viz_frame, bg="white", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Status bar under the canvas
        self.status_label = ttk.Label(
            viz_frame,
            text="Ready",
            style="secondary.TLabel",
            font=("Segoe UI", 10),
        )
        self.status_label.pack(pady=(10, 0), fill=tk.X)
        self.status_label.configure(foreground="#222", background="#f8f9fa")

    def setup_info_panel(self, parent):
        """Set up the right information, statistics, and control panels"""
        info_frame = ttk.Frame(parent)
        info_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(20, 0), expand=True)

        # ----- Information -----
        info_title = ttk.Label(
            info_frame,
            text="Information",
            font=("Segoe UI", 13, "bold"),
            style="info.TLabel",
        )
        info_title.pack(pady=(0, 16))

        dark_mode = self.root.style.theme.name == "superhero"

        text_bg = "#212529" if dark_mode else "#f8f9fa"
        text_fg = "#f8f9fa" if dark_mode else "#222"

        self.info_text = tk.Text(
            info_frame,
            height=8,
            width=40,
            wrap=tk.WORD,
            font=("Segoe UI", 10),
            bg=text_bg,
            relief=tk.FLAT,
        )
        self.info_text.pack(pady=(0, 16), fill=tk.BOTH, expand=True)
        self.info_text.configure(foreground=text_fg)

        # ----- Statistics -----
        stats_frame = ttk.LabelFrame(info_frame, text="Statistics", padding=16)
        stats_frame.pack(fill=tk.X, pady=(0, 16))

        self.stats_text = tk.Text(
            stats_frame,
            height=4,
            width=40,
            wrap=tk.WORD,
            font=("Segoe UI", 10),
            bg=text_bg,
            relief=tk.FLAT,
        )
        self.stats_text.pack(fill=tk.BOTH, expand=True)
        self.stats_text.configure(foreground=text_fg)

        # ----- Step Explanation -----
        explanation_frame = ttk.LabelFrame(
            info_frame, text="Step Explanation", padding=16
        )
        explanation_frame.pack(fill=tk.X, pady=(0, 16))

        self.explanation_text = tk.Text(
            explanation_frame,
            height=4,
            width=40,
            wrap=tk.WORD,
            font=("Segoe UI", 10),
            bg=text_bg,
            relief=tk.FLAT,
        )
        self.explanation_text.pack(fill=tk.BOTH, expand=True)
        self.explanation_text.configure(foreground=text_fg)

        # ----- Example Code -----
        code_frame = ttk.LabelFrame(info_frame, text="Example Code", padding=16)
        code_frame.pack(fill=tk.BOTH, pady=(0, 16), expand=True)

        self.code_text = tk.Text(
            code_frame,
            height=10,
            width=40,
            wrap=tk.NONE,
            font=("Consolas", 9),
            bg=text_bg,
            relief=tk.FLAT,
        )
        self.code_text.pack(fill=tk.BOTH, expand=True)
        self.code_text.configure(foreground=text_fg)

        # Add horizontal scrollbar for code
        h_scroll = ttk.Scrollbar(
            code_frame, orient="horizontal", command=self.code_text.xview
        )
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.code_text.configure(xscrollcommand=h_scroll.set)

        # ----- Controls -----
        controls_frame = ttk.LabelFrame(info_frame, text="Controls", padding=16)
        controls_frame.pack(fill=tk.X, pady=(0, 16), expand=True)

        ttk.Label(controls_frame, text="Speed:", font=("Segoe UI", 10)).pack(
            anchor=tk.W
        )
        self.speed_slider = ttk.Scale(
            controls_frame,
            from_=50,
            to=1000,
            orient="horizontal",
            value=400,
            command=self.on_speed_change,
        )
        self.speed_slider.pack(fill=tk.X, pady=(0, 5))
        self.speed_label = ttk.Label(
            controls_frame, text="400ms", font=("Segoe UI", 10)
        )
        self.speed_label.pack()

        # ----- Data Structure Controls -----
        self.ds_controls_frame = ttk.LabelFrame(
            info_frame, text="Data Structure Controls", padding=16
        )
        self.ds_controls_frame.pack(fill=tk.X, expand=True)

        # Value input
        input_frame = ttk.Frame(self.ds_controls_frame)
        input_frame.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(input_frame, text="Value:", font=("Segoe UI", 10)).pack(side=tk.LEFT)
        self.value_entry = ttk.Entry(input_frame, width=12, font=("Segoe UI", 10))
        self.value_entry.pack(side=tk.LEFT, padx=(8, 8))
        self.value_entry.insert(0, "5")

        # Operation buttons
        op_frame = ttk.Frame(self.ds_controls_frame)
        op_frame.pack(fill=tk.X)

        self.op_btn1 = ttk.Button(
            op_frame,
            text="➕ Insert",
            command=lambda: self.ds_operation("insert"),
            width=10,
            style="success.TButton",
            bootstyle="success-outline rounded",
        )
        self.op_btn1.pack(side=tk.LEFT, padx=(0, 8))
        ToolTip(self.op_btn1, "Insert a value into the data structure")

        self.op_btn2 = ttk.Button(
            op_frame,
            text="❌ Delete",
            command=lambda: self.ds_operation("delete"),
            width=10,
            style="danger.TButton",
            bootstyle="danger-outline rounded",
        )
        self.op_btn2.pack(side=tk.LEFT, padx=(0, 8))
        ToolTip(self.op_btn2, "Delete a value from the data structure")

        self.op_btn3 = ttk.Button(
            op_frame,
            text="🔍 Search",
            command=lambda: self.ds_operation("search"),
            width=10,
            style="info.TButton",
            bootstyle="info-outline rounded",
        )
        self.op_btn3.pack(side=tk.LEFT)
        ToolTip(self.op_btn3, "Search for a value in the data structure")

        # Focus highlight for DS controls and entry
        def _apply_focus_highlight(widget):
            try:
                widget.configure(
                    takefocus=True,
                    highlightthickness=2,
                    highlightbackground="#4F8EF7",
                    highlightcolor="#4F8EF7",
                )
            except tk.TclError:
                widget.configure(takefocus=True)

        for _btn in [self.op_btn1, self.op_btn2, self.op_btn3]:
            _apply_focus_highlight(_btn)

        _apply_focus_highlight(self.value_entry)

    def on_mode_change(self, event=None):
        """Handle mode change"""
        mode = self.mode_var.get()
        if mode == "Sorting Algorithms":
            self.current_mode = "sorting"
            self.algo_combo.configure(values=list(SORTING_ALGORITHMS.keys()))
            self.algo_var.set("Bubble Sort")
        else:
            self.current_mode = "data_structures"
            self.algo_combo.configure(values=list(DATA_STRUCTURES.keys()))
            self.algo_var.set("Linked List")

        self.update_info_panel()
        self.update_explanation(
            "Welcome! Select a mode and press Start to begin the visualization."
        )
        self.reset()

    def on_algorithm_change(self, event=None):
        """Handle algorithm/data structure change"""
        if self.current_mode == "sorting":
            self.current_algorithm = self.algo_var.get()
        else:
            self.current_data_structure = self.algo_var.get()
            self.setup_data_structure()

        self.update_info_panel()
        self.update_explanation(
            "Welcome! Select a mode and press Start to begin the visualization."
        )
        self.reset()

    def on_speed_change(self, value):
        """Handle speed slider change"""
        self.animation_speed = int(float(value))
        self.speed_label.config(text=f"{self.animation_speed}ms")

        # If actively sorting and not paused, re-schedule with new speed immediately
        if self.sorting and not self.paused and self.after_id:
            self.master.after_cancel(self.after_id)
            self.after_id = self.master.after(self.animation_speed, self.sorting_step)

    def on_theme_change(self, event=None):
        """Handle theme change from the theme switcher"""
        new_theme = self.theme_var.get()
        self.root.style.theme_use(new_theme)

    def update_info_panel(self):
        """Update the information panel"""
        self.info_text.delete(1.0, tk.END)

        if self.current_mode == "sorting":
            info = ALGORITHM_INFO[self.current_algorithm]
            text = f"""Algorithm: {self.current_algorithm}

Description:
{info["description"]}

Time Complexity: {info["time_complexity"]}
Space Complexity: {info["space_complexity"]}
Stable: {"Yes" if info["stable"] else "No"}
In-Place: {"Yes" if info["in_place"] else "No"}"""
        else:
            info = DATA_STRUCTURE_INFO[self.current_data_structure]
            text = f"""Data Structure: {self.current_data_structure}

Description:
{info["description"]}

Operations: {", ".join(info["operations"])}

Time Complexity:
"""
            for op, complexity in info["time_complexity"].items():
                text += f"  {op}: {complexity}\n"

        self.info_text.insert(1.0, text)

        # Update example code snippet
        try:
            if self.current_mode == "sorting":
                obj = SORTING_ALGORITHMS[self.current_algorithm]
            else:
                obj = DATA_STRUCTURES[self.current_data_structure]

            src = inspect.getsource(obj)
            # Truncate long source to first 60 lines
            src_lines = src.splitlines()
            if len(src_lines) > 60:
                src = "\n".join(src_lines[:60]) + "\n# ... (truncated) ..."
        except Exception:
            src = "Source code unavailable."

        self.code_text.delete(1.0, tk.END)
        self.code_text.insert(1.0, src)

    def setup_data_structure(self):
        """Initialize the current data structure"""
        ds_class = DATA_STRUCTURES[self.current_data_structure]
        self.data_structure = ds_class()

        # Seed with a few random elements so visualization isn't empty
        sample_count = 7  # Increased from 4 for more substantial structures
        for _ in range(sample_count):
            val = random.randint(1, 20)
            # Try the common insertion methods
            for method_name in ("insert", "push", "enqueue", "insert_at_end"):
                if hasattr(self.data_structure, method_name):
                    method = getattr(self.data_structure, method_name)
                    # Call with generator support but ignore yields here
                    res = method(val)
                    if isinstance(res, types.GeneratorType):
                        list(res)
                    break

        # Immediately draw the seeded structure
        self.draw_visualization()

    def generate_random_data(self):
        """Generate random data for visualization"""
        if self.current_mode == "sorting":
            size = random.randint(5, 15)
            self.data = [random.randint(1, 20) for _ in range(size)]
        else:
            # For data structures, add some random elements
            if self.data_structure:
                for _ in range(random.randint(3, 8)):
                    value = random.randint(1, 20)
                    if hasattr(self.data_structure, "insert"):
                        self.data_structure.insert(value)
                    elif hasattr(self.data_structure, "push"):
                        self.data_structure.push(value)
                    elif hasattr(self.data_structure, "enqueue"):
                        self.data_structure.enqueue(value)

        self.draw_visualization()

    def start_visualization(self):
        """Start the visualization"""
        if self.sorting:
            return

        self.sorting = True
        self.paused = False
        self.step_count = 0
        self.comparisons = 0
        self.swaps = 0

        # Disable controls
        self.start_btn.configure(state="disabled")
        self.reset_btn.configure(state="disabled")
        self.random_btn.configure(state="disabled")

        # Disable other interactive controls during run
        self.pause_btn.configure(state="normal", text="⏸️ Pause")
        self.add_btn.configure(state="disabled")
        self.add_value_entry.configure(state="disabled")

        if self.current_mode == "sorting":
            self.start_sorting_visualization()
        else:
            self.start_ds_visualization()

    def start_sorting_visualization(self):
        """Start sorting algorithm visualization"""
        algorithm = SORTING_ALGORITHMS[self.current_algorithm]
        self.sorting_generator = algorithm(self.data.copy())
        self.sorting_step()

    def start_ds_visualization(self):
        """Run an automatic traversal / search to animate the current data structure"""

        if not self.data_structure:
            return

        # Pick a generator-based operation to visualise
        if hasattr(self.data_structure, "inorder_traversal"):
            self.ds_generator = self.data_structure.inorder_traversal()
            demo_msg = "Inorder traversal"
        elif hasattr(self.data_structure, "search") and self.data_structure.to_array():
            target = self.data_structure.to_array()[0]
            self.ds_generator = self.data_structure.search(target)
            demo_msg = f"Searching for {target}"
        else:
            self.draw_visualization()
            self.update_explanation("No animated traversal available.")
            return

        # Kick off animation
        self.update_explanation(demo_msg)
        self.sorting = True
        self.paused = False
        self.pause_btn.configure(state="normal", text="⏸️ Pause")
        self.ds_step()

    def sorting_step(self):
        """Perform one step of sorting visualization"""
        try:
            if self.paused:
                return  # exit until resumed
            if self.sorting_generator:
                arr, indices, swapped = next(self.sorting_generator)
                self.data = arr.copy()
                self.step_count += 1
                if swapped:
                    self.swaps += 1
                else:
                    self.comparisons += 1

                self.draw_visualization(indices, swapped)
                self.update_statistics()

                # Human-readable explanation
                if swapped and indices and len(indices) == 2:
                    self.update_explanation(
                        f"Swapped elements at positions {indices[0]} and {indices[1]}"
                    )
                elif indices and len(indices) == 2:
                    self.update_explanation(
                        f"Comparing elements at positions {indices[0]} and {indices[1]}"
                    )
                else:
                    self.update_explanation("Processing…")

                # Schedule next step and keep handle for dynamic speed changes
                if self.after_id:
                    self.master.after_cancel(self.after_id)
                self.after_id = self.master.after(
                    self.animation_speed, self.sorting_step
                )
            else:
                self.complete_visualization()
        except StopIteration:
            self.complete_visualization()

    def complete_visualization(self):
        """Complete the visualization"""
        self.sorting = False
        self.paused = False
        self.start_btn.configure(state="normal")
        self.reset_btn.configure(state="normal")
        self.random_btn.configure(state="normal")
        self.pause_btn.configure(state="disabled", text="⏸️ Pause")
        self.add_btn.configure(state="normal")
        self.add_value_entry.configure(state="normal")
        self.status_label.config(text="Visualization Complete!")
        self.pulse_status_label()

    def pulse_status_label(self, count=0):
        """Pulse the status label to animate completion."""
        colors = ["#4CAF50", "#F7B32B", "#E94F37"]
        if count < 6:
            color = colors[count % len(colors)]
            self.status_label.config(foreground=color)
            self.master.after(150, lambda: self.pulse_status_label(count + 1))
        else:
            self.status_label.config(foreground="")

    # ---------------------------------------------------------------------
    # Credits (Star-Wars crawl)
    # ---------------------------------------------------------------------

    def show_credits(self):
        """Display a new window with a scrolling Star-Wars-style credits crawl."""

        credits_lines = [
            "DSA Simulator",  # Title
            "",
            "Developed by:",
            "Your Name Here",  # <- Replace with your actual name(s)
            "",
            "Powered by",
            "Python • Tkinter • ttkbootstrap",
            "",
            "Special Thanks:",
            "OpenAI",  # or any contributors you wish to credit
            "",
            "May the algorithms be with you!",
        ]

        top = tk.Toplevel(self.master)
        top.title("Credits")
        top.geometry("600x600")
        top.configure(bg="black")

        # Close on Escape or click
        top.bind("<Escape>", lambda e: top.destroy())
        top.bind("<Button-1>", lambda e: top.destroy())

        canvas = tk.Canvas(top, bg="black", highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)

        # Initial placement below the visible area
        text_items = []
        start_y = 600 + 20  # 20px padding before first line
        for i, line in enumerate(credits_lines):
            item = canvas.create_text(
                300,  # center X
                start_y + i * 30,
                text=line,
                fill="#FFE81F",  # Star-Wars yellow
                font=("Segoe UI", 16, "bold" if i == 0 else "normal"),
            )
            text_items.append(item)

        # Perform the crawl animation
        def _crawl():
            # Move all text items up
            for tid in text_items:
                canvas.move(tid, 0, -2)  # 2px per frame

            # If the last item has completely left the window, close
            bbox = canvas.bbox(text_items[-1])
            if bbox and bbox[3] < 0:
                top.destroy()
                return

            top.after(40, _crawl)  # ~25 FPS

        _crawl()

    def ds_operation(self, operation):
        """Perform data structure operation"""
        if not self.data_structure:
            return

        try:
            value = int(self.value_entry.get())
        except ValueError:
            return

        # Reset any previous ds generator
        self.ds_generator = None
        message_captured = ""

        # Candidate method names for each generic operation
        method_candidates = {
            "insert": [
                "insert",
                "insert_at_end",
                "insert_at_beginning",
                "push",
                "enqueue",
            ],
            "delete": [
                "delete",
                "delete_node",
                "pop",
                "dequeue",
            ],
            "search": [
                "search",
                "peek",  # treat peek as a read/search op
            ],
        }

        for method_name in method_candidates.get(operation, []):
            if hasattr(self.data_structure, method_name):
                method = getattr(self.data_structure, method_name)
                res = method(value) if method.__code__.co_argcount == 2 else method()
                if isinstance(res, types.GeneratorType):
                    self.ds_generator = res
                    # Start animation loop
                    self.sorting = True
                    self.paused = False
                    self.pause_btn.configure(state="normal", text="⏸️ Pause")
                    self.ds_step()
                else:
                    # Non-generator immediate update
                    self.draw_visualization()
                    self.update_statistics()
                return

        # If no matching method found
        self.update_explanation(f"{operation.capitalize()} not supported.")

    def ds_step(self):
        """Animate data-structure operation generator"""
        if self.paused:
            return

        try:
            if self.ds_generator:
                state, highlight, msg = next(self.ds_generator)
                # state is already stored inside data structure; draw
                self.draw_visualization(highlight)
                self.update_statistics()
                if msg:
                    self.update_explanation(msg)

                # schedule next step
                if self.after_id:
                    self.master.after_cancel(self.after_id)
                self.after_id = self.master.after(self.animation_speed, self.ds_step)
            else:
                self.complete_ds_animation()
        except StopIteration:
            self.complete_ds_animation()

    def complete_ds_animation(self):
        self.sorting = False
        self.paused = False
        self.ds_generator = None
        self.pause_btn.configure(state="disabled", text="⏸️ Pause")

        # Re-enable controls
        self.start_btn.configure(state="normal")
        self.reset_btn.configure(state="normal")
        self.random_btn.configure(state="normal")
        self.add_btn.configure(state="normal")
        self.add_value_entry.configure(state="normal")

        # Draw one last time to clear highlights
        self.draw_visualization()
        self.status_label.config(text="Animation Complete!")

        if self.after_id:
            self.master.after_cancel(self.after_id)
            self.after_id = None

    def draw_visualization(self, highlight_indices=None, swapped=False):
        """Draw the current state visualization"""
        self.canvas.delete("all")

        # Draw gradient background
        self.draw_gradient_bg()

        if self.current_mode == "sorting":
            self.draw_sorting_visualization(highlight_indices, swapped)
        else:
            self.draw_ds_visualization(highlight_indices)

    def draw_gradient_bg(self):
        """Draw a vertical gradient background on the canvas for visual appeal."""
        canvas_width = self.canvas.winfo_width() or 800
        canvas_height = self.canvas.winfo_height() or 400
        for i in range(canvas_height):
            r1, g1, b1 = 244, 244, 244  # #F4F4F4
            r2, g2, b2 = 194, 233, 251  # #C2E9FB
            r = int(r1 + (r2 - r1) * i / canvas_height)
            g = int(g1 + (g2 - g1) * i / canvas_height)
            b = int(b1 + (b2 - b1) * i / canvas_height)
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.canvas.create_line(0, i, canvas_width, i, fill=color)

    def draw_sorting_visualization(self, highlight_indices=None, swapped=False):
        """Draw sorting algorithm visualization"""
        if not self.data:
            return

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width <= 1:  # Canvas not yet sized
            canvas_width = 800
            canvas_height = 400

        bar_width = max(30, (canvas_width - 100) // len(self.data))
        max_val = max(self.data) if self.data else 1

        # Enhanced color palette
        default_color = "#4F8EF7"  # Blue
        compare_color = "#F7B32B"  # Yellow
        swap_color = "#E94F37"  # Red
        complete_color = "#4CAF50"  # Green

        # Draw bars
        for i, value in enumerate(self.data):
            x = 50 + i * bar_width
            height = int((value / max_val) * (canvas_height - 100))
            y = canvas_height - 50 - height

            # Choose color based on highlighting
            if highlight_indices and i in highlight_indices:
                color = swap_color if swapped else compare_color
            else:
                color = default_color

            # 3-D bar: front + top + side faces
            # Front face
            self.canvas.create_rectangle(
                x,
                y,
                x + bar_width - 5,
                canvas_height - 50,
                fill=color,
                outline="",
                width=0,
            )

            # Helper to lighten/darken a hex color
            def _adjust(hex_color, factor=0.8):
                hex_color = hex_color.lstrip("#")
                r, g, b = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
                r = int(min(255, r * factor))
                g = int(min(255, g * factor))
                b = int(min(255, b * factor))
                return f"#{r:02x}{g:02x}{b:02x}"

            top_color = _adjust(color, 1.2)
            side_color = _adjust(color, 0.6)

            # Top face (slanted)
            self.canvas.create_polygon(
                x,
                y,
                x + 6,
                y - 6,
                x + bar_width - 5 + 6,
                y - 6,
                x + bar_width - 5,
                y,
                fill=top_color,
                outline="",
            )

            # Side face
            self.canvas.create_polygon(
                x + bar_width - 5,
                y,
                x + bar_width - 5 + 6,
                y - 6,
                x + bar_width - 5 + 6,
                canvas_height - 50 - 6,
                x + bar_width - 5,
                canvas_height - 50,
                fill=side_color,
                outline="",
            )

            # Draw value
            self.canvas.create_text(
                x + bar_width // 2,
                canvas_height - 30,
                text=str(value),
                font=("Segoe UI", 11, "bold"),
            )

    def draw_ds_visualization(self, highlight_indices=None):
        """Draw data structure visualization"""
        if not self.data_structure:
            return

        data = self.data_structure.to_array()
        if not data:
            return

        canvas_width = self.canvas.winfo_width() or 800
        canvas_height = self.canvas.winfo_height() or 400

        node_color = "#4F8EF7"
        text_color = "white"

        if self.current_data_structure in ("Binary Tree", "Binary Heap"):
            # Tree layout using array representation indices
            radius = 20
            level_height = 80

            for idx, value in enumerate(data):
                if value is None:
                    continue

                level = int(math.log2(idx + 1)) if idx else 0
                nodes_in_level = 2**level
                position_in_level = idx - (2**level - 1)

                # Horizontal spacing within the level
                gap = canvas_width // (nodes_in_level + 1)
                x = gap * (position_in_level + 1)
                y = 50 + level * level_height

                # Helper to adjust color brightness
                def _adjust(hex_color, factor=0.8):
                    hex_color = hex_color.lstrip("#")
                    r, g, b = [int(hex_color[i : i + 2], 16) for i in (0, 2, 4)]
                    r = int(min(255, r * factor))
                    g = int(min(255, g * factor))
                    b = int(min(255, b * factor))
                    return f"#{r:02x}{g:02x}{b:02x}"

                # Highlight check
                is_highlight = highlight_indices and idx in highlight_indices
                base_color = "#E94F37" if is_highlight else node_color
                top_c = _adjust(base_color, 1.2)
                side_c = _adjust(base_color, 0.6)

                # Front face (circle)
                self.canvas.create_oval(
                    x - radius,
                    y - radius,
                    x + radius,
                    y + radius,
                    fill=base_color,
                    outline="",
                )

                # Simple top highlight (smaller lighter ellipse)
                self.canvas.create_oval(
                    x - radius + 4,
                    y - radius + 4,
                    x + radius - 8,
                    y + radius - 8,
                    fill=top_c,
                    outline="",
                )

                # Side shading (right darker semi-ellipse)
                self.canvas.create_oval(
                    x - 4,
                    y - radius + 2,
                    x + radius,
                    y + radius - 2,
                    fill=side_c,
                    outline="",
                )

                # Draw edge to parent
                if idx != 0:
                    parent_idx = (idx - 1) // 2
                    parent_level = int(math.log2(parent_idx + 1))
                    parent_pos_in_level = parent_idx - (2**parent_level - 1)
                    parent_gap = canvas_width // (2**parent_level + 1)
                    parent_x = parent_gap * (parent_pos_in_level + 1)
                    parent_y = 50 + parent_level * level_height

                    self.canvas.create_line(
                        parent_x,
                        parent_y + radius,
                        x,
                        y - radius,
                        fill="#333",
                        width=2,
                    )
        else:
            # Linear structures (Array, Stack, Queue, Linked List)
            element_width = 60
            spacing = 20
            start_x = 50

            for i, value in enumerate(data):
                x = start_x + i * (element_width + spacing)
                y = canvas_height // 2

                def _adjust(hex_color, factor=0.8):
                    hex_color = hex_color.lstrip("#")
                    r, g, b = [int(hex_color[i : i + 2], 16) for i in (0, 2, 4)]
                    r = int(min(255, r * factor))
                    g = int(min(255, g * factor))
                    b = int(min(255, b * factor))
                    return f"#{r:02x}{g:02x}{b:02x}"

                # Highlight check
                is_highlight = highlight_indices and i in highlight_indices
                base_color = "#E94F37" if is_highlight else node_color
                top_c = _adjust(base_color, 1.2)
                side_c = _adjust(base_color, 0.6)

                # Front face
                self.canvas.create_rectangle(
                    x,
                    y - 20,
                    x + element_width,
                    y + 20,
                    fill=base_color,
                    outline="",
                )

                # Top face (slanted)
                self.canvas.create_polygon(
                    x,
                    y - 20,
                    x + 4,
                    y - 24,
                    x + element_width + 4,
                    y - 24,
                    x + element_width,
                    y - 20,
                    fill=top_c,
                    outline="",
                )

                # Side face
                self.canvas.create_polygon(
                    x + element_width,
                    y - 20,
                    x + element_width + 4,
                    y - 24,
                    x + element_width + 4,
                    y + 20 - 4,
                    x + element_width,
                    y + 20,
                    fill=side_c,
                    outline="",
                )

                self.canvas.create_text(
                    x + element_width // 2,
                    y,
                    text=str(value),
                    font=("Segoe UI", 12, "bold"),
                    fill=text_color,
                )

                # Connection for linked list
                if self.current_data_structure == "Linked List" and i < len(data) - 1:
                    next_x = start_x + (i + 1) * (element_width + spacing)
                    self.canvas.create_line(
                        x + element_width,
                        y,
                        next_x,
                        y,
                        fill="#333",
                        width=2,
                        arrow=tk.LAST,
                    )

    def update_statistics(self):
        """Update the statistics display"""
        self.stats_text.delete(1.0, tk.END)

        if self.current_mode == "sorting":
            stats = f"""Steps: {self.step_count}
Comparisons: {self.comparisons}
Swaps: {self.swaps}
Array Size: {len(self.data)}"""
        else:
            if self.data_structure:
                data = self.data_structure.to_array()
                stats = f"""Elements: {len(data)}
Data Structure: {self.current_data_structure}
Current State: {data}"""
            else:
                stats = "No data structure initialized"

        self.stats_text.insert(1.0, stats)

    def update_explanation(self, message: str):
        """Display a short textual explanation of the current step/operation."""
        if not hasattr(self, "explanation_text"):
            return
        self.explanation_text.delete(1.0, tk.END)
        self.explanation_text.insert(tk.END, message)

    def reset(self):
        """Reset the visualization"""
        self.sorting = False
        self.paused = False
        self.step_count = 0
        self.comparisons = 0
        self.swaps = 0

        # Re-enable controls
        self.start_btn.configure(state="normal")
        self.reset_btn.configure(state="normal")
        self.random_btn.configure(state="normal")
        self.pause_btn.configure(state="disabled", text="⏸️ Pause")
        self.add_btn.configure(state="normal")
        self.add_value_entry.configure(state="normal")

        if self.current_mode == "sorting":
            self.data = [12, 8, 14, 19, 2, 7, 1, 3, 17, 4]
        else:
            self.setup_data_structure()

        self.draw_visualization()
        self.update_statistics()
        self.update_explanation(
            "Welcome! Select a mode and press Start to begin the visualization."
        )
        self.status_label.config(text="Ready")

    # ------------------------------------------------------------------
    # Pause / Resume & Add Value
    # ------------------------------------------------------------------

    def toggle_pause(self):
        """Toggle pause/resume state during sorting visualization."""
        if not self.sorting:
            return

        self.paused = not self.paused
        new_text = "▶️ Resume" if self.paused else "⏸️ Pause"
        self.pause_btn.configure(text=new_text)

        # If resuming, kick off the next step
        if not self.paused:
            # kick off with current speed
            if self.after_id:
                self.master.after_cancel(self.after_id)
            self.after_id = self.master.after(self.animation_speed, self.sorting_step)

    def add_value(self):
        """Append a new value to the array when in sorting mode."""
        if self.current_mode != "sorting" or self.sorting:
            return

        try:
            val = int(self.add_value_entry.get())
        except ValueError:
            return

        self.data.append(val)
        self.draw_visualization()
        self.update_statistics()

    def setup_info_panel(self, parent):
        """Set up the right information, statistics, and control panels"""
        info_frame = ttk.Frame(parent)
        info_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(20, 0), expand=True)

        # ----- Information -----
        info_title = ttk.Label(
            info_frame,
            text="Information",
            font=("Segoe UI", 13, "bold"),
            style="info.TLabel",
        )
        info_title.pack(pady=(0, 16))

        dark_mode = self.root.style.theme.name == "superhero"

        text_bg = "#212529" if dark_mode else "#f8f9fa"
        text_fg = "#f8f9fa" if dark_mode else "#222"

        self.info_text = tk.Text(
            info_frame,
            height=8,
            width=40,
            wrap=tk.WORD,
            font=("Segoe UI", 10),
            bg=text_bg,
            relief=tk.FLAT,
        )
        self.info_text.pack(pady=(0, 16), fill=tk.BOTH, expand=True)
        self.info_text.configure(foreground=text_fg)

        # ----- Statistics -----
        stats_frame = ttk.LabelFrame(info_frame, text="Statistics", padding=16)
        stats_frame.pack(fill=tk.X, pady=(0, 16))

        self.stats_text = tk.Text(
            stats_frame,
            height=4,
            width=40,
            wrap=tk.WORD,
            font=("Segoe UI", 10),
            bg=text_bg,
            relief=tk.FLAT,
        )
        self.stats_text.pack(fill=tk.BOTH, expand=True)
        self.stats_text.configure(foreground=text_fg)

        # ----- Step Explanation -----
        explanation_frame = ttk.LabelFrame(
            info_frame, text="Step Explanation", padding=16
        )
        explanation_frame.pack(fill=tk.X, pady=(0, 16))

        self.explanation_text = tk.Text(
            explanation_frame,
            height=4,
            width=40,
            wrap=tk.WORD,
            font=("Segoe UI", 10),
            bg=text_bg,
            relief=tk.FLAT,
        )
        self.explanation_text.pack(fill=tk.BOTH, expand=True)
        self.explanation_text.configure(foreground=text_fg)

        # ----- Example Code -----
        code_frame = ttk.LabelFrame(info_frame, text="Example Code", padding=16)
        code_frame.pack(fill=tk.BOTH, pady=(0, 16), expand=True)

        self.code_text = tk.Text(
            code_frame,
            height=10,
            width=40,
            wrap=tk.NONE,
            font=("Consolas", 9),
            bg=text_bg,
            relief=tk.FLAT,
        )
        self.code_text.pack(fill=tk.BOTH, expand=True)
        self.code_text.configure(foreground=text_fg)

        # Add horizontal scrollbar for code
        h_scroll = ttk.Scrollbar(
            code_frame, orient="horizontal", command=self.code_text.xview
        )
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.code_text.configure(xscrollcommand=h_scroll.set)

        # ----- Controls -----
        controls_frame = ttk.LabelFrame(info_frame, text="Controls", padding=16)
        controls_frame.pack(fill=tk.X, pady=(0, 16), expand=True)

        ttk.Label(controls_frame, text="Speed:", font=("Segoe UI", 10)).pack(
            anchor=tk.W
        )
        self.speed_slider = ttk.Scale(
            controls_frame,
            from_=50,
            to=1000,
            orient="horizontal",
            value=400,
            command=self.on_speed_change,
        )
        self.speed_slider.pack(fill=tk.X, pady=(0, 5))
        self.speed_label = ttk.Label(
            controls_frame, text="400ms", font=("Segoe UI", 10)
        )
        self.speed_label.pack()

        # ----- Data Structure Controls -----
        self.ds_controls_frame = ttk.LabelFrame(
            info_frame, text="Data Structure Controls", padding=16
        )
        self.ds_controls_frame.pack(fill=tk.X, expand=True)

        # Value input
        input_frame = ttk.Frame(self.ds_controls_frame)
        input_frame.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(input_frame, text="Value:", font=("Segoe UI", 10)).pack(side=tk.LEFT)
        self.value_entry = ttk.Entry(input_frame, width=12, font=("Segoe UI", 10))
        self.value_entry.pack(side=tk.LEFT, padx=(8, 8))
        self.value_entry.insert(0, "5")

        # Operation buttons
        op_frame = ttk.Frame(self.ds_controls_frame)
        op_frame.pack(fill=tk.X)

        self.op_btn1 = ttk.Button(
            op_frame,
            text="➕ Insert",
            command=lambda: self.ds_operation("insert"),
            width=10,
            style="success.TButton",
            bootstyle="success-outline rounded",
        )
        self.op_btn1.pack(side=tk.LEFT, padx=(0, 8))
        ToolTip(self.op_btn1, "Insert a value into the data structure")

        self.op_btn2 = ttk.Button(
            op_frame,
            text="❌ Delete",
            command=lambda: self.ds_operation("delete"),
            width=10,
            style="danger.TButton",
            bootstyle="danger-outline rounded",
        )
        self.op_btn2.pack(side=tk.LEFT, padx=(0, 8))
        ToolTip(self.op_btn2, "Delete a value from the data structure")

        self.op_btn3 = ttk.Button(
            op_frame,
            text="🔍 Search",
            command=lambda: self.ds_operation("search"),
            width=10,
            style="info.TButton",
            bootstyle="info-outline rounded",
        )
        self.op_btn3.pack(side=tk.LEFT)
        ToolTip(self.op_btn3, "Search for a value in the data structure")

        # Focus highlight for DS controls and entry
        def _apply_focus_highlight(widget):
            try:
                widget.configure(
                    takefocus=True,
                    highlightthickness=2,
                    highlightbackground="#4F8EF7",
                    highlightcolor="#4F8EF7",
                )
            except tk.TclError:
                widget.configure(takefocus=True)

        for _btn in [self.op_btn1, self.op_btn2, self.op_btn3]:
            _apply_focus_highlight(_btn)

        _apply_focus_highlight(self.value_entry)

        # Footer
        footer = ttk.Label(
            self.master, text="© 2024 DSA Simulator", style="secondary.TLabel"
        )
        footer.pack(side=tk.BOTTOM, fill=tk.X)


def main():
    """Main function to run the DSA Simulator"""
    # Fixed to the 'superhero' theme for a slick dark look
    root = ttk.Window(themename="superhero")
    app = DSASimulator(root)
    root.mainloop()


if __name__ == "__main__":
    main()

