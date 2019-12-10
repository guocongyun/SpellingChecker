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

def click_event():
    pass

def generate_interface():
    generating_story("forest.png", "please select your character")
    generate_decisions(0)
    activate_mouse()

def generating_story(image_file, text):
    canvas.create_text(window_width / 2 + h, h, fill="white", font="Times 10 bold", text=text, anchor=NW)
    image = PhotoImage(file=image_file)
    image = image.subsample(3)
    # scale_w = new_width / old_width
    # scale_h = new_height / old_height
    # photoImg.zoom(scale_w, scale_h)
    canvas.create_image(h, h, image=image, anchor=NW)

def click_event(event):
    x = event.x
    y = event.y
    history = []
    for i in range(len(xy[0])):
        if xy[0][i][0] <= x <= xy[0][i][2] and xy[0][i][1] <= y <= xy[0][i][3]:
            print("button", i, "clicked")
            light_area(decisions, i)
            canvas.after(500, dim_area, decisions, i)

def character_creation():
    # players
    xy[0].append([2 * w, 15 * h, 6 * w, 21 * h])
    decisions.append(canvas.create_rectangle(xy[0][4], fill="grey", outline='black'))
    xy[1].append(
        [4 * w - characters_size[0][0] / 2, 16 * h, 4 * w + characters_size[0][0] / 2, 16 * h + characters_size[0][1]])
    characters.append(canvas.create_rectangle(xy[1][0], fill="white"))

    xy[0].append([6 * w, 15 * h, 10 * w, 21 * h])
    decisions.append(canvas.create_rectangle(xy[0][5], fill="grey", outline='black'))
    xy[1].append(
        [8 * w - characters_size[1][0] / 2, 16 * h, 8 * w + characters_size[1][0] / 2, 16 * h + characters_size[1][1]])
    characters.append(canvas.create_oval(xy[1][1], fill="white"))

    xy[0].append([2 * w, 21 * h, 6 * w, 27 * h])
    decisions.append(canvas.create_rectangle(xy[0][6], fill="grey", outline='black'))
    xy[1].append(
        [4 * w - characters_size[2][0] / 2, 22 * h, 4 * w + characters_size[2][0] / 2, 22 * h + characters_size[2][1]])
    characters.append(canvas.create_rectangle(xy[1][2], fill="white"))

    # text
    xy[0].append([6 * w, 21 * h, 10 * w, 27 * h])
    decisions.append(canvas.create_rectangle(xy[0][7], fill="grey", outline='black'))
    characters.append(canvas.create_text(7.9 * w, 23 * h, text="In progress..."))

    # # enemy
    # xy[1].append([4 * w - characters_size[2][0] / 2, 22 * h, 4 * w + characters_size[2][0] / 2, 22 * h + characters_size[2][1]])
    # characters.append(canvas.create_rectangle(xy[1][2], fill="white"))

    for i in range(len(xy[1])):
        print(canvas.bbox(characters[i]))

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
characters = []
characters_attribute = [
    [1, 1, 1, 1, 10],
    [1, 1, 1, 1, 10],
    [2, 1, 2, 1, 10],
    [0, 0, 0, 0, 0]
]
characters_size = [
    [30, 30, 1],
    [900 ** (1 / 2), 30, 1],
    [450 ** (1 / 2), 2 * 450 ** (1 / 2), 2],
    [0, 0]
]
window, window_width, window_height = configuring_window()
unit_width, unit_height, w, h = defining_units()
canvas = configuring_canvas()
generate_interface()
character_creation()
window.mainloop()
