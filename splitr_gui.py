from splitr import split_audio
import tkinter as tk
from tkinter import filedialog
from splitr import split_audio  # Assuming your splitr functions are correctly modularized and importable

def browse_file():
    filename = filedialog.askopenfilename(filetypes=(("Audio files", "*.mp3;*.wav"), ("All files", "*.*")))
    file_path_entry.delete(0, tk.END)
    file_path_entry.insert(0, filename)

def start_processing():
    file_path = file_path_entry.get()
    start_time = start_time_entry.get()
    try:
        split_audio(file_path, start_time)
        output_text.insert(tk.END, "Processing completed successfully!\n")
    except Exception as e:
        output_text.insert(tk.END, f"Error: {str(e)}\n")

app = tk.Tk()
app.title("Splitr GUI")

# File Path
tk.Label(app, text="File Path:").pack()
file_path_entry = tk.Entry(app, width=50)
file_path_entry.pack(padx=20, pady=5)
browse_button = tk.Button(app, text="Browse", command=browse_file)
browse_button.pack()

# Start Time
tk.Label(app, text="Start Time (hh:mm:ss):").pack()
start_time_entry = tk.Entry(app, width=20)
start_time_entry.pack(padx=20, pady=5)

# Start Button
start_button = tk.Button(app, text="Start Processing", command=start_processing)
start_button.pack(pady=20)

# Output Text Area
output_text = tk.Text(app, height=10, width=50)
output_text.pack(padx=20, pady=20)

app.mainloop()
