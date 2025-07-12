import ttkbootstrap as ttk
from sorting_visualizer import SortingVisualizer

# Entry point for the application
if __name__ == "__main__":
    root = ttk.Window(themename="cosmo")  # Create the main window with Bootstrap theme
    root.title("Data Structures & Algorithms Visualizer")  # Set window title
    SortingVisualizer(root)  # Initialize and pack the visualizer UI
    root.mainloop()  # Start the Tkinter event loop
