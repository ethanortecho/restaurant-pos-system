

from tkinter import *



width = 1920  # Width of the monitor
height = 1080  # Height of the monitor
x_offset = 1920  # Start at the right edge of the primary monitor
y_offset = 0  # Start at the top of the screen
root = Tk()
root.title("CityBird POS System")
root.geometry(f"{width}x{height}+{x_offset}+{y_offset}")


root.mainloop()
