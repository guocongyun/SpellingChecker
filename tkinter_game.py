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

def defining_units():
    unit_width = window_width / 12
    unit_height = window_height / 30
    w = unit_width
    h = unit_height
    return unit_width, unit_height, w, h

def activate_mouse():
    canvas.bind("<Button-1>", click_event)

def generate_decisions(scenario):
    # choice 4 boxes choices
    for i in range(4):
        if i < 2:
            xy[0].append([2 * w + i * 4 * w, 9 * h, 2 * w + (i + 1) * 4 * w, 10 * h])
            decisions.append(canvas.create_rectangle(xy[0][i], fill="grey", outline='black'))
            decisions.append(
                canvas.create_text(window_width / 3 + i * window_width / 3, window_height / 60 + 9 * h, fill="white",
                                   font="Times 10", text=choices[scenario][i]))
        else:
            xy[0].append([2 * w + (i - 2) * 4 * w, 10 * h, 2 * w + (i - 1) * 4 * w, 11 * h])
            decisions.append(canvas.create_rectangle(xy[0][i], fill="grey", outline='black'))
            decisions.append(
                canvas.create_text(window_width / 3 + (i - 2) * window_width / 3, window_height / 60 + 10 * h,
                                   fill="white",
                                   font="Times 10", text=choices[scenario][i]))


def light_area(list, option):
    canvas.itemconfigure(list[option], fill="red")


def dim_area(list, option):
    canvas.itemconfigure(list[option], fill="grey")


def deactivate_mouse():
    canvas.unbind("<Button-1>")

def configuring_canvas():
    canvas = Canvas(window, bg="black", width=window_width, height=window_height)
    canvas.pack()
    return canvas

xy = [[], []]
position = []
decisions = []
choices = [
    ["Please choose a character", "Please choose a character", "Please choose a character", "Please choose a character"]
]
window, window_width, window_height = configuring_window()
unit_width, unit_height, w, h = defining_units()
canvas = configuring_canvas()
window.mainloop()
