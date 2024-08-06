import tkinter as tk

# Create the main application window
root = tk.Tk()
root.title("Scrollable Frame Example")

# Create a frame to hold the canvas and scrollbar
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=1)

# Create a canvas widget
canvas = tk.Canvas(main_frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

# Add a vertical scrollbar to the frame
scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configure the canvas to work with the scrollbar
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Create another frame inside the canvas to hold the content
scrollable_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# Add some sample content to the scrollable frame
for i in range(50):
    tk.Label(scrollable_frame, text=f"Sample content {i+1}").pack()

# Run the application
root.mainloop()