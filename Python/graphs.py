import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
import matplotlib.pyplot as plt

# Global list to store dynamically created Entry widgets
entry_list = []

# Function to clear dynamically created Entry fields
def clear_dynamic_entries():
    global entry_list
    for entry in entry_list:
        entry.destroy()  # Remove the entry widget from the interface
    entry_list = []  # Clear the list


# Function to handle scatter plot input prompt
def prompt_scatter_points():
    clear_dynamic_entries()  # Clear any previous dynamically created entries

    try:
        # Ask the user for the number of points needed
        num_points = simpledialog.askinteger("Scatter Plot", "How many points do you want to plot?", minvalue=2)

        if num_points:
            # Dynamically create entry fields for each point's y-value
            for i in range(1, num_points + 1):
                label = tk.Label(root, text=f"Enter value for Point {i}:")
                label.grid(row=i + 5, column=0, padx=10, pady=5)
                entry = tk.Entry(root)
                entry.grid(row=i + 5, column=1, padx=10, pady=5)
                entry_list.append(entry)  # Add the entry to the list for later reference

    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number of points.")

# Function to validate entry values
def validate_entries(entries):
    values = []
    for entry in entries:
        try:
            value = float(entry.get().strip())
            values.append(value)
        except ValueError:
            raise ValueError(f"Invalid value in entry: {entry.get().strip()}")
    return values

# Function to get custom plot styles
def get_custom_plot_styles():
    marker = simpledialog.askstring("Marker Style", "Enter marker style (e.g., 'o', 'x', '^'): ", initialvalue='o')
    color = simpledialog.askstring("Color", "Enter color (e.g., 'blue', 'red', '#FF5733'): ", initialvalue='blue')
    return marker, color

# Function to prompt for scatter y-axis label
def prompt_scatter_yaxis_label():
    return simpledialog.askstring("Y-Axis Label", "Enter a label for the Y-axis:")

# Function to plot the graph
def plot_graph():
    try:
        if plot_type.get() == "scatter":
            if not entry_list:
                messagebox.showerror("Input Error", "Please input values for the scatter plot.")
                return

            # Collect values for scatter plot
            y_values = validate_entries(entry_list)
            x_values = list(range(1, len(y_values) + 1))

            y_label = prompt_scatter_yaxis_label()
            marker, color = get_custom_plot_styles()

            # Plot scatter graph
            plt.figure(figsize=(5, 4))
            plt.scatter(x_values, y_values, color=color, marker=marker, label='Input Scatter')

        else:
            # Handle line or bar plot (assume 2 points from fixed entry1 and entry2)
            num1 = float(entry1.get().strip())
            num2 = float(entry2.get().strip())
            x_values = [1, 2]
            y_values = [num1, num2]

            plt.figure(figsize=(5, 4))
            if plot_type.get() == "line":
                plt.plot(x_values, y_values, marker='o', color='b', linestyle='--', label='Input Line')
            elif plot_type.get() == "bar":
                plt.bar(x_values, y_values, color='g', label='Input Bar')

        plt.title("Custom Graph")
        plt.xlabel("Index")
        plt.ylabel("Value")
        plt.grid(True)
        plt.legend()
        plt.show()

        clear_entries()

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers.")

# Function to save the graph
def save_graph():
    try:
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"),
                                                            ("PDF files", "*.pdf"),
                                                            ("JPEG files", "*.jpeg"),
                                                            ("All Files", "*.*")])
        if file_path:
            if plot_type.get() == "scatter":
                y_values = validate_entries(entry_list)
                x_values = list(range(1, len(y_values) + 1))
                plt.scatter(x_values, y_values, color='r', label='Saved Scatter')
            else:
                num1 = float(entry1.get().strip())
                num2 = float(entry2.get().strip())
                x_values = [1, 2]
                y_values = [num1, num2]

                plt.figure(figsize=(5, 4))
                if plot_type.get() == "line":
                    plt.plot(x_values, y_values, marker='o', color='r', linestyle='--', label='Saved Line')
                elif plot_type.get() == "bar":
                    plt.bar(x_values, y_values, color='g', label='Saved Bar')

            plt.title("Saved Graph")
            plt.xlabel("Index")
            plt.ylabel("Value")
            plt.grid(True)
            plt.legend()
            plt.savefig(file_path)
            messagebox.showinfo("Success", f"Graph saved as {file_path}")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers.")

# Function to clear the input fields
def clear_entries():
    entry1.delete(0, tk.END)
    entry2.delete(0, tk.END)
    clear_dynamic_entries()  # Clear dynamic scatter point entries as well

# Function to load input values from file for line/bar plots
def load_from_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("CSV Files", "*.csv"), ("All Files", "*.*")])
    if file_path:
        try:
            with open(file_path, "r") as file:
                data = file.read().strip().split(",")  # Assuming values are comma-separated
                if len(data) != 2:
                    raise ValueError("File must contain exactly two numbers.")
                entry1.delete(0, tk.END)
                entry2.delete(0, tk.END)
                entry1.insert(0, data[0])
                entry2.insert(0, data[1])
        except Exception as e:
            messagebox.showerror("File Error", f"Error loading file: {e}")

# Function to load scatter data from a file
def load_scatter_from_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("CSV Files", "*.csv"), ("All Files", "*.*")])
    if file_path:
        try:
            with open(file_path, "r") as file:
                data = file.read().strip().split(",")
                clear_dynamic_entries()
                for i, value in enumerate(data):
                    label = tk.Label(root, text=f"Point {i+1}:")
                    label.grid(row=i + 5, column=0, padx=10, pady=5)
                    entry = tk.Entry(root)
                    entry.insert(0, value)
                    entry.grid(row=i + 5, column=1, padx=10, pady=5)
                    entry_list.append(entry)
        except Exception as e:
            messagebox.showerror("File Error", f"Error loading scatter plot: {e}")

# Function to confirm window close
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

# Function to show help menu
def show_help():
    help_text = """Instructions:
    1. Select the type of plot you want (Line, Bar, Scatter).
    2. Enter values for Line/Bar, or click Scatter to input multiple points.
    3. Click 'Plot Graph' to visualize the data.
    4. Use 'Save Graph' to save the plot as PNG, PDF, etc.
    5. Load data from a file for Line/Bar or Scatter plots."""
    messagebox.showinfo("Help", help_text)

# Create the main window
root = tk.Tk()
root.title("Custom Graphs")
root.geometry("400x400")
root.resizable(True, True)

# Create the menu bar
menu = tk.Menu(root)
root.config(menu=menu)

help_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="Instructions", command=show_help)

# Create and place labels and entries for user input
label1 = tk.Label(root, text="Enter First Number:")
label1.grid(row=0, column=0, padx=10, pady=5, sticky="e")

entry1 = tk.Entry(root)
entry1.grid(row=0, column=1, padx=10, pady=5)

label2 = tk.Label(root, text="Enter Second Number:")
label2.grid(row=1, column=0, padx=10, pady=5, sticky="e")

entry2 = tk.Entry(root)
entry2.grid(row=1, column=1, padx=10, pady=5)

# Variable to store the selected plot type
plot_type = tk.StringVar(value="line")

# Create radio buttons for plot type selection
radio_line = tk.Radiobutton(root, text="Line Plot", variable=plot_type, value="line")
radio_line.grid(row=2, column=0, sticky="w")

radio_bar = tk.Radiobutton(root, text="Bar Plot", variable=plot_type, value="bar")
radio_bar.grid(row=2, column=1, sticky="w")

radio_scatter = tk.Radiobutton(root, text="Scatter Plot", variable=plot_type, value="scatter", command=prompt_scatter_points)
radio_scatter.grid(row=2, column=2, sticky="w")

# Create buttons to interact with the application
plot_button = tk.Button(root, text="Plot Graph", command=plot_graph)
plot_button.grid(row=3, column=0, pady=10)

save_button = tk.Button(root, text="Save Graph", command=save_graph)
save_button.grid(row=3, column=1)

clear_button = tk.Button(root, text="Clear", command=clear_entries)
clear_button.grid(row=3, column=2)

load_button = tk.Button(root, text="Load From File", command=load_from_file)
load_button.grid(row=4, column=0)

load_scatter_button = tk.Button(root, text="Load Scatter Data", command=load_scatter_from_file)
load_scatter_button.grid(row=4, column=1)

# Add functionality to confirm window close
root.protocol("WM_DELETE_WINDOW", on_closing)

# Run the Tkinter event loop
root.mainloop()
