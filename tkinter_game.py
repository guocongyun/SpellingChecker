from tkinter import *


def configuring_window():
    window = Tk()
    window.title("tkintergame")
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight() - 90
    window_width = 800
    window_height = screen_height
    center_width = screen_width / 2 - window_width / 2
    center_height = 0
    window.geometry("%dx%d+%d+%d" % (window_width, window_height, center_width, center_height))
    return window, window_width, window_height


def configuring_canvas():
    canvas = Canvas(window, bg="black", width=window_width, height=window_height)
    canvas.pack()
    return canvas


window, window_width, window_height = configuring_window()
canvas = configuring_canvas()
window.mainloop()
