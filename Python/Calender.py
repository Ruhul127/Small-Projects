import tkinter as tk
from tkinter import ttk
import calendar
from tkinter import messagebox
from datetime import datetime
import json  # For persistent notes

# Dictionary to store notes for specific dates
notes = {}

# Load notes from the JSON file (persistent notes)
def load_notes_from_file():
    global notes
    try:
        with open('notes.json', 'r') as file:
            notes = json.load(file)
    except FileNotFoundError:
        notes = {}

# Save notes to a JSON file
def save_notes_to_file():
    with open('notes.json', 'w') as file:
        json.dump(notes, file)

# Current theme variable
current_theme = "Light"

# Function to apply the selected theme
def apply_theme(theme):
    global current_theme
    current_theme = theme
    
    style = ttk.Style()
    if theme == "Light":
        root.config(bg="white")
        cal_frame.config(bg="white")
        input_frame.config(bg="white")
        style.configure('TButton', background='lightgray', foreground='black')
        style.configure('TLabel', background='white', foreground='black')
    elif theme == "Dark":
        root.config(bg="black")
        cal_frame.config(bg="black")
        input_frame.config(bg="black")
        style.configure('TButton', background='gray', foreground='white')
        style.configure('TLabel', background='black', foreground='white')

# Function to display the calendar for a specific month and year
def show_calendar():
    try:
        # Validate year and month input
        year = int(year_entry.get())
        month = int(month_entry.get())
        
        if year < 2000:
            raise ValueError("Year must be 2000 or later")
        
        if month < 1 or month > 12:
            raise ValueError("Month must be between 1 and 12")
    except ValueError as e:
        messagebox.showerror("Invalid Input", f"Invalid input: {e}")
        return

    # Clear the calendar frame before creating new buttons
    for widget in cal_frame.winfo_children():
        widget.destroy()

    # Generate the days in the selected month and year
    month_days = calendar.monthcalendar(year, month)
    
    # Highlight today's date
    today = datetime.today()
    
    # Create calendar grid (weekdays header)
    days_of_week = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    for day in days_of_week:
        tk.Label(cal_frame, text=day, padx=10, pady=10, font=("Arial", 10, "bold"), 
                 bg="white" if current_theme == "Light" else "black", 
                 fg="black" if current_theme == "Light" else "white").grid(row=0, column=days_of_week.index(day))

    # Add the following code inside the show_calendar function, after the days_of_week loop:
    for week_num, week in enumerate(month_days):
        for day_num, day in enumerate(week):
            if day == 0:  # Empty cell (day does not exist)
                continue
            date_key = (year, month, day)

            # Check if a note exists for the day to change button style
            if date_key in notes:
                day_button = tk.Button(cal_frame, text=str(day), padx=10, pady=10, 
                                           command=lambda d=day: open_note_window(year, month, d),
                                           bg="lightgreen" if current_theme == "Light" else "darkgreen")  # Green if note exists
            else:
                day_button = tk.Button(cal_frame, text=str(day), padx=10, pady=10, 
                                           command=lambda d=day: open_note_window(year, month, d),
                                           bg="lightgray" if current_theme == "Light" else "gray")  # Gray if no note

            # Change the background color of the button if the day is Sunday (day_num == 0)
            if day_num == 0:
                day_button.config(bg="red")  # Red for Sunday

            # Highlight today's date
            if year == today.year and month == today.month and day == today.day:
                day_button.config(bg="yellow")

            day_button.grid(row=week_num + 1, column=day_num)

# Function to open a new window for adding/viewing notes for a specific date
def open_note_window(year, month, day):
    # Create a new window
    note_window = tk.Toplevel(root)
    note_window.title(f"Notes for {day}/{month}/{year}")

    # Date label
    date_label = ttk.Label(note_window, text=f"Date: {day}/{month}/{year}", font=("Arial", 12))
    date_label.pack(pady=5)

    # Text box for writing the note
    note_text = tk.Text(note_window, height=10, width=40)
    note_text.pack(pady=5)

    # If a note already exists for this date, populate the text box
    date_key = (year, month, day)
    if date_key in notes:
        note_text.insert(tk.END, notes[date_key])

    # Save button to store the note
    def save_note():
        note_content = note_text.get("1.0", tk.END).strip()
        if note_content:
            notes[date_key] = note_content  # Store the note
        else:
            if date_key in notes:
                if messagebox.askyesno("Delete Note", "Are you sure you want to delete this note?"):
                    del notes[date_key]  # Remove note if text box is empty
        note_window.destroy()
        save_notes_to_file()

    # Auto-save when window is closed
    def on_close():
        save_note()

    note_window.protocol("WM_DELETE_WINDOW", on_close)

    save_button = ttk.Button(note_window, text="Save Note", command=save_note)
    save_button.pack(pady=5)

# Function to display all notes in a new window
def view_all_notes():
    if not notes:
        messagebox.showinfo("No Notes", "No notes have been added yet.")
        return
    
    # Create a new window to display all notes
    notes_window = tk.Toplevel(root)
    notes_window.title("All Notes")
    
    # Create a scrollable frame for the notes
    canvas = tk.Canvas(notes_window)
    scroll_y = tk.Scrollbar(notes_window, orient="vertical", command=canvas.yview)
    scroll_frame = ttk.Frame(canvas)
    
    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scroll_y.set)
    
    # Search box
    search_label = ttk.Label(scroll_frame, text="Search Notes:")
    search_label.pack(pady=5)
    search_entry = ttk.Entry(scroll_frame)
    search_entry.pack(pady=5)
    
    def search_notes():
        search_query = search_entry.get().lower()
        for widget in scroll_frame.winfo_children():
            widget.destroy()

        for date_key, note_content in notes.items():
            year, month, day = date_key
            if search_query in note_content.lower() or search_query in f"{day}/{month}/{year}":
                date_label = ttk.Label(scroll_frame, text=f"Date: {day}/{month}/{year}", font=("Arial", 10, "bold"))
                date_label.pack(pady=5)
                note_label = tk.Label(scroll_frame, text=note_content, wraplength=300, justify="left", bg="lightyellow", padx=5, pady=5)
                note_label.pack(fill="x", padx=10, pady=5)

    search_button = ttk.Button(scroll_frame, text="Search", command=search_notes)
    search_button.pack(pady=5)
    
    canvas.pack(side="left", fill="both", expand=True)
    scroll_y.pack(side="right", fill="y")

# Previous and next month navigation
def show_next_month():
    current_month = int(month_entry.get())
    current_year = int(year_entry.get())
    if current_month == 12:
        year_entry.delete(0, tk.END)
        year_entry.insert(0, str(current_year + 1))
        month_entry.delete(0, tk.END)
        month_entry.insert(0, "1")
    else:
        month_entry.delete(0, tk.END)
        month_entry.insert(0, str(current_month + 1))
    show_calendar()

def show_prev_month():
    current_month = int(month_entry.get())
    current_year = int(year_entry.get())
    if current_month == 1:
        year_entry.delete(0, tk.END)
        year_entry.insert(0, str(current_year - 1))
        month_entry.delete(0, tk.END)
        month_entry.insert(0, "12")
    else:
        month_entry.delete(0, tk.END)
        month_entry.insert(0, str(current_month - 1))
    show_calendar()

# Jump to the current date
def jump_to_current_date():
    today = datetime.today()
    year_entry.delete(0, tk.END)
    month_entry.delete(0, tk.END)
    year_entry.insert(0, today.year)
    month_entry.insert(0, today.month)
    show_calendar()

# Initialise the main tkinter window
root = tk.Tk()
root.title("Calendar")
root.geometry("400x550")

# Frame for user input
input_frame = ttk.Frame(root)
input_frame.pack(pady=10)

# Labels and Entry fields for year and month
year_label = ttk.Label(input_frame, text="Enter Year:")
year_label.grid(row=0, column=0, padx=5)

year_entry = ttk.Entry(input_frame)
year_entry.grid(row=0, column=1, padx=5)

month_label = ttk.Label(input_frame, text="Enter Month (1-12):")
month_label.grid(row=1, column=0, padx=5)

month_entry = ttk.Entry(input_frame)
month_entry.grid(row=1, column=1, padx=5)

# Autofill today's date
today = datetime.today()
year_entry.insert(0, today.year)
month_entry.insert(0, today.month)

# Show calendar button
show_button = ttk.Button(input_frame, text="Show Calendar", command=show_calendar)
show_button.grid(row=2, columnspan=2, pady=10)

# Previous and next month buttons
prev_button = ttk.Button(input_frame, text="Previous Month", command=show_prev_month)
prev_button.grid(row=3, column=0, pady=10)

next_button = ttk.Button(input_frame, text="Next Month", command=show_next_month)
next_button.grid(row=3, column=1, pady=10)

# Jump to today button
jump_button = ttk.Button(input_frame, text="Jump to Today", command=jump_to_current_date)
jump_button.grid(row=4, columnspan=2, pady=10)

# Button to view all notes
view_notes_button = ttk.Button(root, text="View All Notes", command=view_all_notes)
view_notes_button.pack(pady=10)

# Dropdown for theme selection
theme_label = ttk.Label(root, text="Select Theme:")
theme_label.pack(pady=5)

theme_var = tk.StringVar(value="Light")
theme_dropdown = ttk.OptionMenu(root, theme_var, "Light", "Dark", command=apply_theme)
theme_dropdown.pack(pady=5)

# Frame for the calendar display
cal_frame = ttk.Frame(root)
cal_frame.pack(pady=10)

# Load notes on start
load_notes_from_file()

# Start the tkinter main loop
root.mainloop()
