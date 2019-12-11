from random import randint
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

def character_movement():
    global direction, collide
    check_character_boarder()
    if direction == "left":
        canvas.move(characters[0], collide[0]*-characters_attribute[0][1], 0)
    elif direction == "right":
        canvas.move(characters[0], collide[1]*characters_attribute[0][3], 0)
    elif direction == "up":
        canvas.move(characters[0], 0, collide[2]*-characters_attribute[0][0])
    elif direction == "down":
        canvas.move(characters[0], 0, collide[3]*characters_attribute[0][2])
        # repeat movement

def check_character_boarder():
    global position
    position = canvas.coords(characters[0])
    if position[0] < 0:
        canvas.coords(characters[0], window_width, position[1],
                      window_width - characters_size[0][0], position[3])
    elif position[2] > window_width:
        canvas.coords(characters[0], characters_size[0][0], position[1], 0, position[3])
    elif position[3] > window_height:
        canvas.coords(characters[0], position[0], 8 * h + characters_size[0][1], position[2], 8 * h)
    elif position[1] < 8 * h:
        canvas.coords(characters[0], position[0], window_height, position[2],
                      window_height - characters_size[0][1])
    global collide
    for enemy_i in range(len(xy[1])-1):
        enemy_i = enemy_i + 1
        position_i = canvas.coords(characters[enemy_i])
        if position_i[0] < position[2] and position_i[2] > position[0] and position_i[1] < position[
            3] and position_i[3] > position[1]:
            if position[0] > position_i[0]:
                collide[0] = -5
            if position[2] < position_i[2]:
                collide[1] = -5
            if position[1] < position_i[1]:
                collide[3] = -5
            if position[3] > position_i[3]:
                collide[2] = -5

def click_event(event):
    x = event.x
    y = event.y
    history = []
    for i in range(len(xy[0])):
        if xy[0][i][0] <= x <= xy[0][i][2] and xy[0][i][1] <= y <= xy[0][i][3]:
            print("button", i, "clicked")
            light_area(decisions, i)
            canvas.after(500, dim_area, decisions, i)
            if 3 < i < 7:
                clear_screen(i - 4)
                delete_unused_characters(i - 4)
                deactivate_mouse()
                move_start_position()
                activate_keyboard()
                character_movement()
                enemy_creation()
                enemy_movement()


def enemy_creation():
    global characters, characters_attribute, characters_size
    number_of_enemy = difficulty  # randint(2,20)
    weak_enemy = 1 + int(number_of_enemy / 10)
    strong_enemy = number_of_enemy - weak_enemy
    position = canvas.coords(characters)
    enemy = 0
    while enemy < number_of_enemy:
        overlap = False
        if enemy < weak_enemy:
            print(characters_size)
            enemy_size = characters_size[0][0] * characters_size[0][1] - 100
            color = "yellow"
        else:
            enemy_size = characters_size[0][0] * characters_size[0][1] + 100 * (enemy - weak_enemy)
            color = "purple"
        enemy_width = enemy_size ** (1 / 2)
        enemy_height = enemy_size ** (1 / 2)
        enemy_x_pos = randint(0, int(window_width - enemy_width))
        enemy_y_pos = randint(8 * int(h), 26 * int(h))
        enemy_position = [enemy_x_pos, enemy_y_pos, enemy_x_pos + enemy_width, enemy_y_pos + enemy_height]
        for character in xy[1]:
            if character[0] < enemy_position[2] and character[2] > enemy_position[0] \
                    and character[1] < enemy_position[3] and character[3] > enemy_position[1]:
                overlap = True
        if not overlap:
            xy[1].append(enemy_position)
            characters.append(canvas.create_rectangle(xy[1][enemy + 1], fill=color))
            characters_size.append([enemy_width, enemy_height])
            characters_attribute.append([1, 1, 3])
            enemy += 1

def key_pressed(event):
    global direction, key
    print(key)
    if event.keysym == "Left":
        direction = "left"
        key[0] = 1
    elif event.keysym == "Right":
        direction = "right"
        key[1] = 1
    elif event.keysym == "Up":
        direction = "up"
        key[2] = 1
    elif event.keysym == "Down":
        direction = "down"
        key[3] = 1

def check_enemy_boarder():
    global characters_attribute, count, collide
    for enemy_i in range(len(xy[1])-1):
        enemy_i = enemy_i + 1
        count = 1
        position_i = canvas.coords(characters[enemy_i])
        if position_i[0] <= 0:
            characters_attribute[enemy_i][0] = -characters_attribute[enemy_i][0]
        elif position_i[2] >= window_width:
            characters_attribute[enemy_i][0] = -characters_attribute[enemy_i][0]
        elif position_i[3] >= window_height:
            characters_attribute[enemy_i][1] = -characters_attribute[enemy_i][1]
        elif position_i[1] <= 8 * h:
            characters_attribute[enemy_i][1] = -characters_attribute[enemy_i][1]
        else:
            count -= 1
            for enemy_j in range(len(xy[1])):
                if enemy_i != enemy_j:
                    position_j = canvas.coords(characters[enemy_j])
                    if position_i[0] < position_j[2] and position_i[2] > position_j[0] and position_i[1] < position_j[
                        3] and position_i[3] > position_j[1]:
                        # if position_j[0] <= position_i[0] < position_j[2] or position_j[0] <= position_i[2] < position_j[2]:
                        #     if position_j[1] <= position_i[1] < position_j[3] or position_j[1] <= position_i[3] < position_j[3]:\
                        # counts[character_i] += 1
                        count += 1
                        if count <= 1:
                            characters_attribute[enemy_i ][0] = -characters_attribute[enemy_i ][0]
                            characters_attribute[enemy_i ][1] = -characters_attribute[enemy_i ][1]

def enemy_movement():
    check_enemy_boarder()
    for character in range(len(characters) - 1):
        enemy = character + 1
        canvas.move(characters[enemy], characters_attribute[enemy][0], characters_attribute[enemy][1])
    canvas.after(characters_attribute[1][2], enemy_movement)

def key_released(event):
    global direction, key
    if sum(key) <= 1:
        direction = "0"
    if event.keysym == "Left":
        key[0] = 0
    if event.keysym == "Right":
        key[1] = 0
    if event.keysym == "Up":
        key[2] = 0
    if event.keysym == "Down":
        key[3] = 0


def activate_keyboard():
    canvas.bind("<KeyPress>", key_pressed)
    canvas.bind("<KeyRelease>", key_released)
    canvas.focus_set()


def deactivate_keyboard():
    canvas.unbind("<Down>")
    canvas.unbind("<Up>")
    canvas.unbind("<Right>")
    canvas.unbind("<Left>")


def move_start_position():
    global position
    position = canvas.coords(characters[0])
    if position[0] < 6 * w - characters_size[0][0] / 2 - 2:
        canvas.move(characters[0], 1, 0)
        canvas.after(5, move_start_position)
    elif position[0] > 6 * w - characters_size[0][0] / 2 + 2:
        canvas.move(characters[0], -1, 0)
        canvas.after(5, move_start_position)
    elif position[1] < 30 * h - characters_size[0][1] - 2:
        canvas.move(characters[0], 0, 1)
        canvas.after(5, move_start_position)
    elif position[1] > 30 * h - characters_size[0][1] + 2:
        canvas.move(characters[0], 0, -1)
        canvas.after(5, move_start_position)

def clear_screen(choice):
    for item in range(len(decisions)):
        canvas.delete(decisions[item])
    for item in range(len(characters)):
        if item != choice:
            canvas.delete(characters[item])

def delete_unused_characters(choice):
    global characters, characters_attribute, characters_size
    characters = [characters[choice]]
    characters_attribute = [characters_attribute[choice]]
    characters_size = [characters_size[choice]]
    xy[1] = [xy[1][choice]]
    # while len(characters) > 1:
    #     for x in range(len(characters)):
    #         print(x)
    #         print(characters)
    #         print(choice)
    #         print(choice - count)
    #         if characters[x] != characters[choice - count]:
    #             characters.remove(characters[x])
    #             characters_size.remove(characters_size[x])
    #             characters_attribute.remove(characters_attribute[x])

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
