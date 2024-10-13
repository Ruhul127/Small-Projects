import tkinter as tk
from tkinter import messagebox


class TimeTrackingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Time Tracking for Lessons")
        self.root.geometry("400x300")
        
        self.lesson_duration = tk.IntVar(value=45)  # Default lesson duration is 45 minutes
        self.time_remaining = 0
        self.timer_running = False
        
        # User interface elements
        self.label = tk.Label(root, text="Time Remaining:", font=("Arial", 18))
        self.label.pack(pady=10)
        
        self.time_display = tk.Label(root, text="00:00", font=("Arial", 48))
        self.time_display.pack(pady=10)
        
        # Set Lesson Duration
        self.duration_label = tk.Label(root, text="Set Lesson Duration (minutes):", font=("Arial", 12))
        self.duration_label.pack(pady=5)

        self.duration_entry = tk.Entry(root, textvariable=self.lesson_duration, font=("Arial", 12), width=5)
        self.duration_entry.pack(pady=5)
        
        # Start, Reset, and Pause Buttons
        self.start_button = tk.Button(root, text="Start", command=self.start_timer, font=("Arial", 14))
        self.start_button.pack(side=tk.LEFT, padx=20, pady=10)
        
        self.reset_button = tk.Button(root, text="Reset", command=self.reset_timer, font=("Arial", 14))
        self.reset_button.pack(side=tk.LEFT, padx=20, pady=10)
        
        self.pause_button = tk.Button(root, text="Pause", command=self.pause_timer, font=("Arial", 14))
        self.pause_button.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Fullscreen Toggle Button
        self.fullscreen_button = tk.Button(root, text="Full-Screen", command=self.toggle_fullscreen, font=("Arial", 14))
        self.fullscreen_button.pack(side=tk.LEFT, padx=20, pady=10)
        
        self.update_clock()

    def start_timer(self):
        if not self.timer_running:
            self.time_remaining = self.lesson_duration.get() * 60
            self.timer_running = True

    def reset_timer(self):
        self.timer_running = False
        self.time_remaining = 0
        self.update_clock()

    def pause_timer(self):
        self.timer_running = False

    def update_clock(self):
        if self.timer_running and self.time_remaining > 0:
            minutes = self.time_remaining // 60
            seconds = self.time_remaining % 60
            self.time_display.config(text=f"{minutes:02d}:{seconds:02d}")
            self.time_remaining -= 1
            self.root.after(1000, self.update_clock)
        elif self.time_remaining == 0 and self.timer_running:
            messagebox.showinfo("Time's up", "Lesson complete!")
            self.timer_running = False
        else:
            minutes = self.time_remaining // 60
            seconds = self.time_remaining % 60
            self.time_display.config(text=f"{minutes:02d}:{seconds:02d}")
            self.root.after(1000, self.update_clock)

    def toggle_fullscreen(self):
        self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen"))


if __name__ == "__main__":
    root = tk.Tk()
    app = TimeTrackingApp(root)
    root.mainloop()
