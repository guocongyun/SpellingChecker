import os
from datetime import time
from tkinter import *
from random import *
from PIL import Image, ImageTk

# configuring window
from PIL.Image import ANTIALIAS

window = Tk()
window.title("tkintergame")
screen_width = window.winfo_screenwidth()
screen_height = 1000
window_width = 800
window_height = screen_height
center_width = screen_width / 2 - window_width / 2
center_height = 0
window.geometry("%dx%d+%d+%d" % (window_width, window_height, center_width, center_height))
w = window_width / 12
h = window_height / 30

# configuring canvas
canvas = Canvas(window, bg="black", width=window_width, height=window_height)
canvas.pack(fill="both", expand=TRUE)


# The Data above are all constants

class Battle:
    def generating_statistic(self):
        try:
            canvas.delete(game_system.score_identifier)
        except:
            pass
        try:
            canvas.delete(game_system.level_identifier)
        except:
            pass
        try:
            for number in range(len(game_system.life_identifier)):
                canvas.delete(game_system.life_identifier[number])
        except:
            pass

        self.life = Image.open("pixel_heart.png")
        # self.life = life.resize((int(GameSystem.texture_size[0]), int(GameSystem.texture_size[1])), Image.ANTIALIAS)
        self.life = ImageTk.PhotoImage(self.life)

        for number in range(game_system.life):
            game_system.life_identifier.append(
                canvas.tag_raise(canvas.create_image(h + number * 30, h, image=self.life, anchor=NW)))

        game_system.score_identifier = canvas.create_text(window_width - 100, h, fill="white", font="Times 10 bold",
                                                          text="Score : " + str(game_system.score), anchor=NW)
        game_system.level_identifier = canvas.create_text(6 * w, h, fill="white", font="Times 10 bold",
                                                          text="Level-" + str(game_system.level), anchor=NW)

        return self.life

    def move_start_position(self):
        self.position = canvas.coords(game_system.character[0].identifier)
        if (self.position[0] + self.position[2]) / 2 < float(self.start_position[0]) - 2:
            canvas.move(game_system.character[0].identifier, 1, 0)
            canvas.after(5, self.move_start_position)
        elif (self.position[0] + self.position[2]) / 2 > float(self.start_position[0]) + 2:
            canvas.move(game_system.character[0].identifier, -1, 0)
            canvas.after(5, self.move_start_position)
        elif (self.position[1] + self.position[3]) / 2 < float(self.start_position[1]) - 2:
            canvas.move(game_system.character[0].identifier, 0, 1)
            canvas.after(5, self.move_start_position)
        elif (self.position[1] + self.position[3]) / 2 > float(self.start_position[1]) + 2:
            canvas.move(game_system.character[0].identifier, 0, -1)
            canvas.after(5, self.move_start_position)
        else:
            game_system.save_game = False
            self.character_movement()
            self.enemy_creation()
            self.enemy_movement()
            self.character_ability()

    class normal_enemy:

        def __init__(self, character_size):
            self.character_attribute = [1, 1, 3]
            self.character_height = character_size ** (1 / 2)
            self.character_width = character_size ** (1 / 2)
            self.character_size = character_size

    def enemy_creation(self):
        number_of_enemy = game_system.level + 5
        weak_enemy = 1 + int(number_of_enemy / 10)
        enemy_count = 0
        while enemy_count < number_of_enemy:
            overlap = False
            if enemy_count < weak_enemy:
                character_size = (game_system.character[0].character_width * game_system.character[
                    0].character_height - 200) * game_system.scale_factor
                color = "yellow"
            else:
                character_size = (game_system.character[0].character_width * game_system.character[
                    0].character_height + 200 * (enemy_count - weak_enemy)) * game_system.scale_factor
                color = "#cc" + str(99 - int(80 / (number_of_enemy - weak_enemy)) * enemy_count) + "ff"
                if len(str(99 - int(80 / (number_of_enemy - weak_enemy)) * enemy_count)) < 2:
                    color = "purple"
            enemy = self.normal_enemy(character_size)
            enemy_x_pos = randint(0, int(window_width - enemy.character_width))
            enemy_y_pos = randint(0, 26 * int(h))
            enemy_position = [enemy_x_pos, enemy_y_pos, enemy_x_pos + enemy.character_width,
                              enemy_y_pos + enemy.character_height]
            for number in range(len(game_system.character) - 1):
                existing_position = game_system.character[number + 1].xy
                if existing_position[0] < enemy_position[2] and existing_position[2] > enemy_position[0] \
                        and existing_position[1] < enemy_position[3] and existing_position[3] > enemy_position[1]:
                    overlap = True
            if not overlap:
                enemy.color = color
                enemy.xy = enemy_position
                enemy.identifier = canvas.create_rectangle(enemy.xy, fill=color)
                game_system.character.append(enemy)
                enemy_count += 1

    def character_growth(self):
        game_system.score = game_system.score + 10
        self.life = self.generating_statistic()
        game_system.character[0].character_size = game_system.character[
                                                      0].character_size * game_system.scale_factor + 200 * game_system.difficulty * game_system.scale_factor
        if game_system.player_choice == 0:
            game_system.character[0].character_height = game_system.character[0].character_size ** (1 / 2)
            game_system.character[0].character_width = game_system.character[0].character_size ** (1 / 2)
        elif game_system.player_choice == 1:
            game_system.character[0].character_height = game_system.character[0].character_size ** (1 / 2)
            game_system.character[0].character_width = game_system.character[0].character_size ** (1 / 2)
        elif game_system.player_choice == 2:
            game_system.character[0].character_height = (game_system.character[0].character_size / 3) ** (1 / 2)
            game_system.character[0].character_width = (game_system.character[0].character_size / 3) ** (1 / 2) * 3
        elif game_system.player_choice == 3:
            game_system.character[0].character_height = game_system.character[0].character_size ** (1 / 2)
            game_system.character[0].character_width = game_system.character[0].character_size ** (1 / 2)
        else:
            pass
        position = canvas.coords(game_system.character[0].identifier)
        center_position = [(position[0] + position[2]) / 2, (position[1] + position[3]) / 2]
        new_position = [
            center_position[0] - game_system.character[0].character_width / 2,
            center_position[1] - game_system.character[0].character_height / 2,
            center_position[0] + game_system.character[0].character_width / 2,
            center_position[1] + game_system.character[0].character_height / 2
        ]
        game_system.character[0].xy = new_position
        canvas.coords(game_system.character[0].identifier, game_system.character[0].xy)
        self.enemy_recolor()

    def enemy_recolor(self):
        for number in range(len(game_system.character) - 1):
            enemy_number = number + 1
            if game_system.pause or self.ability == "stop":
                canvas.itemconfig(game_system.character[enemy_number].identifier, fill="grey")
            if not game_system.pause and self.ability != "stop":
                canvas.itemconfig(game_system.character[enemy_number].identifier,
                                  fill=game_system.character[enemy_number].color)
            if game_system.character[enemy_number].character_size < game_system.character[0].character_size:
                canvas.itemconfig(game_system.character[enemy_number].identifier, fill="yellow")

    def check_character_boarder(self):
        if game_system.life > 0:
            self.character_save = open("character_saves.txt", "w+")
            position = canvas.coords(game_system.character[0].identifier)
            self.character_save.write(str(game_system.score))
            self.character_save.write("\n" + str(game_system.life))
            self.character_save.write("\n" + str((position[0] + position[2]) / 2 * game_system.scale_factor))
            self.character_save.write("\n" + str((position[1] + position[3]) / 2 * game_system.scale_factor))
        if game_system.entry.get() != "":
            self.character_save.write("\n" + str(game_system.entry.get()))
        else:
            self.character_save.write("\n" + "bob")
        self.character_save.write("\n" + str(game_system.player_choice))
        self.character_save.write("\n" + str(game_system.level+1))

        self.character_save.close()

        if position[0] < 0:
            canvas.coords(game_system.character[0].identifier, window_width, position[1],
                          window_width - game_system.character[0].character_width, position[3])
        elif position[2] > window_width:
            canvas.coords(game_system.character[0].identifier, game_system.character[0].character_width, position[1], 0,
                          position[3])
        elif position[3] > window_height:
            canvas.coords(game_system.character[0].identifier, position[0],
                          8 * h + game_system.character[0].character_height,
                          position[2],
                          8 * h)
        elif position[1] < 0:
            canvas.coords(game_system.character[0].identifier, position[0], window_height, position[2],
                          window_height - game_system.character[0].character_height)
        removed_character = 0
        for character_i in range(len(game_system.character) - 1):
            character_i = character_i + 1 - removed_character
            position_i = canvas.coords(game_system.character[character_i].identifier)
            if position_i[0] < position[2] and position_i[2] > position[0] and position_i[1] < position[
                3] and position_i[3] > position[1]:

                if game_system.character[character_i].character_size < game_system.character[
                    0].character_size or game_system.cheat == True:
                    canvas.delete(game_system.character[character_i].identifier)
                    game_system.character.remove(game_system.character[character_i])
                    self.character_growth()
                    removed_character += 1
                else:
                    self.lose_life()
                    if position[0] > position_i[0]:
                        self.collide[0] = -5
                    if position[2] < position_i[2]:
                        self.collide[1] = -5
                    if position[1] < position_i[1]:
                        self.collide[3] = -5
                    if position[3] > position_i[3]:
                        self.collide[2] = -5

    def check_enemy_boarder(self):
        removed_character = 0
        self.saved_file = open("enemy_saves.txt", "w+")
        for character_i in range(len(game_system.character) - 1):
            character_i = character_i + 1 - removed_character
            count = 1
            position_i = canvas.coords(game_system.character[character_i].identifier)

            # save_position_i = []
            # current_score = self.score
            for number in range(4):
                self.saved_file.write("\n" + str(position_i[number] * game_system.scale_factor))

            if position_i[0] <= 0:
                game_system.character[character_i].character_attribute[0] = - \
                    game_system.character[character_i].character_attribute[0]
            elif position_i[2] >= window_width:
                game_system.character[character_i].character_attribute[0] = - \
                    game_system.character[character_i].character_attribute[0]
            elif position_i[3] >= window_height:
                game_system.character[character_i].character_attribute[1] = - \
                    game_system.character[character_i].character_attribute[1]
            elif position_i[1] <= 0:
                game_system.character[character_i].character_attribute[1] = - \
                    game_system.character[character_i].character_attribute[1]
            else:
                count -= 1
                for character_j in range(len(game_system.character)):
                    character_j = character_j - removed_character
                    if character_i != character_j:
                        position_j = canvas.coords(game_system.character[character_j].identifier)
                        if position_i[0] < position_j[2] and position_i[2] > position_j[0] and position_i[1] < \
                                position_j[3] and position_i[3] > position_j[1]:
                            if character_j == 0:
                                if game_system.character[character_i].character_size < game_system.character[
                                    character_j].character_size or game_system.cheat == True:
                                    canvas.delete(game_system.character[character_i].identifier)
                                    game_system.character.remove(game_system.character[character_i])
                                    removed_character += 1
                                    self.character_growth()
                                    break
                                else:
                                    self.lose_life()
                            count += 1
                            if count <= 1:
                                game_system.character[character_i].character_attribute[0] = - \
                                    game_system.character[character_i].character_attribute[0]
                                game_system.character[character_i].character_attribute[1] = - \
                                    game_system.character[character_i].character_attribute[1]
        self.saved_file.close()

    def lose_life(self):
        game_system.life = game_system.life - 1
        self.life = self.generating_statistic()
        if game_system.life <= 0:
            game_system.lose = True
            self.game_running = False

    def character_movement(self):
        if game_system.game_running:
            if not game_system.pause:
                self.check_character_boarder()
                if self.direction == "left":
                    canvas.move(game_system.character[0].identifier,
                                game_system.scale_factor * self.collide[0] * -
                                game_system.character[0].character_attribute[
                                    1], 0)
                elif self.direction == "right":
                    canvas.move(game_system.character[0].identifier,
                                game_system.scale_factor * self.collide[1] *
                                game_system.character[0].character_attribute[
                                    3], 0)
                elif self.direction == "up":
                    canvas.move(game_system.character[0].identifier, 0,
                                game_system.scale_factor * self.collide[2] * -
                                game_system.character[0].character_attribute[
                                    0])
                elif self.direction == "down":
                    canvas.move(game_system.character[0].identifier, 0,
                                game_system.scale_factor * self.collide[3] *
                                game_system.character[0].character_attribute[
                                    2])
                    # repeat movement
                self.collide = [1, 1, 1, 1]
            canvas.after(game_system.character[0].character_attribute[4], self.character_movement)

    def enemy_movement(self):
        if game_system.game_running:
            self.check_enemy_boarder()
            if not game_system.pause and self.ability != "stop":
                if len(game_system.character) == 1:
                    game_system.win = True
                    game_system.game_running = False
                else:
                    for character in range(len(game_system.character) - 1):
                        enemy = character + 1
                        canvas.move(game_system.character[enemy].identifier,
                                    game_system.scale_factor * game_system.character[enemy].character_attribute[0],
                                    game_system.scale_factor * game_system.character[enemy].character_attribute[1])
            canvas.after(10, self.enemy_movement)

    def character_ability(self):
        if game_system.character[0].ability == "bend_time":
            self.ability_mechanism += 1
            frequency = randint(0, 50)
            if self.ability_mechanism >= frequency:
                self.ability = "stop"
                self.enemy_recolor()
                self.ability_mechanism = 0
            if self.ability_mechanism == 4 and self.ability == "stop":
                self.ability = "continue"
                self.enemy_recolor()
                self.ability_mechanism = 0
            canvas.after(1000, self.character_ability)

    def __init__(self):
        self.start_position = [6 * w, 29 * h]
        self.position = []
        self.collide = [1, 1, 1, 1]
        self.key = [0, 0, 0, 0]
        self.direction = "0"
        self.ability = False
        self.ability_mechanism = 0
        self.character_ability
        self.life = None


class TextAdventure:

    def generating_texture(self, change_color):
        if self.theme == []:
            styles = [3, 2, 1, 1, 3, 2, 1, 6, 0, 0, 0, 3, 5, 4]
            random = randint(0, 6)
            texture_num_a = styles[random] + 1
            texture_num_b = styles[-random - 1] + 1
            while texture_num_a == texture_num_b:
                texture_num_a = randint(0, 4)
            self.theme.append(texture_num_a)
            self.theme.append(texture_num_b)

        self.texture_a = Image.open("tile_" + str(self.theme[0]) + "_full.png")
        self.texture_b = Image.open("tile_" + str(self.theme[1]) + "_full.png")
        self.texture_a = self.texture_a.resize((int(GameSystem.texture_size[0]), int(GameSystem.texture_size[1])),
                                               Image.ANTIALIAS)
        self.texture_a = ImageTk.PhotoImage(self.texture_a)
        self.texture_b = self.texture_b.resize((int(GameSystem.texture_size[0]), int(GameSystem.texture_size[1])),
                                               Image.ANTIALIAS)
        self.texture_b = ImageTk.PhotoImage(self.texture_b)
        count = 0
        for number in range(int(window_height / GameSystem.texture_size[1])):

            #
            height = GameSystem.texture_size[1] * number
            if int(window_width / GameSystem.texture_size[0]) % 2 == 0:
                count += 1
            for number in range(int(window_width / GameSystem.texture_size[0])):
                width = GameSystem.texture_size[0] * number
                count += 1
                if count % 2 == 0:
                    canvas.tag_lower(canvas.create_image(width, height, image=self.texture_a, anchor=NW))
                else:
                    canvas.tag_lower(canvas.create_image(width, height, image=self.texture_b, anchor=NW))
        return self.texture_b, self.texture_a

    def generating_story(self):
        if len(game_system.design) > 0:
            for number in range(len(game_system.design)):
                canvas.delete(game_system.design[number].identifier)
                canvas.delete(game_system.design[number].identifier_text)
                game_system.design = []
        if len(game_system.character) > 0:
            for number in range(len(game_system.character)):
                canvas.delete(game_system.character[number].identifier)
                game_system.character = []

    def clear_screen(self):
        try:
            for number in range(len(game_system.character)):
                if number != game_system.player_choice:
                    canvas.delete(game_system.character[number].identifier)
        except:
            pass
        try:
            if game_system.player_choice != "":
                game_system.character = [game_system.character[game_system.player_choice]]
        except:
            pass
        try :
            for number in range(len(game_system.design)):
                    canvas.delete(game_system.design[number].identifier)
        except:
            pass
        try:
            for number in range(len(game_system.design)):
                    canvas.delete(game_system.design[number].identifier_text)
        except:
            pass
        if len(game_system.identifier) > 0:
            for number in range(len(game_system.identifier)):
                canvas.delete(game_system.identifier[number])

    class Player:
        def __init__(self, size, width, height, attribute):
            self.character_size = size
            self.character_width = width
            self.character_height = height
            self.character_attribute = attribute

    class Box:
        def creating_text_box(self, index):
            center_position = [(game_system.design[index].xy[0] + game_system.design[index].xy[2]) / 2,
                               (game_system.design[index].xy[1] + game_system.design[index].xy[3]) / 2]
            # game_system.design[index].identifier = canvas.create_rectangle(game_system.design[index].xy,
            #                                                                outline='black')
            game_system.design[index].identifier = canvas.create_text(center_position, fill="white",
                                                                      font="Times 10",
                                                                      text=game_system.design[index].text[0])
            center_position[1] = center_position[1] + 15
            game_system.design[index].identifier_text = canvas.create_text(center_position, fill="white",
                                                                           font="Times 10",
                                                                           text=game_system.design[index].text[1])

        def __init__(self, xy, text=[]):
            self.xy = xy
            self.text = text

    def character_boxes(self):
        # creating Box
        game_system.design.append(self.Box([3 * w, 12 * h, 6 * w, 18 * h], ["He is fast", "maybe a bit too fast"]))
        game_system.design.append(self.Box([6 * w, 12 * h, 9 * w, 18 * h], ["Brave and Fearless", "he never go back"]))
        game_system.design.append(self.Box([3 * w, 18 * h, 6 * w, 24 * h], ["Only good", "at moving horizontally"]))
        game_system.design.append(self.Box([6 * w, 18 * h, 9 * w, 24 * h], ["He bends time", "randomly"]))

        for number in range(4):
            self.Box.creating_text_box(self, number)
            # GameSystem.design[number].identifier = canvas.create_rectangle(GameSystem.design[number].xy, fill="grey", outline='black')
            # GameSystem.design[number].identifier = canvas.create_rectangle(GameSystem.design[number].xy, fill="grey", outline='black')

    def character_creation(self):
        game_system.character.append(self.Player(900, 900 ** (1 / 2), 900 ** (1 / 2), [10, 10, 10, 10, 10]))
        game_system.character[0].xy = [4.5 * w - game_system.character[0].character_width / 2,
                                       13.5 * h,
                                       4.5 * w + game_system.character[0].character_width / 2,
                                       13.5 * h + game_system.character[0].character_height]
        game_system.character[0].identifier = (canvas.create_rectangle(game_system.character[0].xy, fill="white"))
        game_system.character[0].ability = "Teleport"

        game_system.character.append(self.Player(900, 900 ** (1 / 2), 900 ** (1 / 2), [5, 3, 0, 3, 10]))
        game_system.character[1].xy = [7.5 * w - game_system.character[1].character_width / 2,
                                       13.5 * h,
                                       7.5 * w + game_system.character[1].character_width / 2,
                                       13.5 * h + game_system.character[1].character_height]
        game_system.character[1].identifier = (canvas.create_oval(game_system.character[1].xy, fill="white"))
        game_system.character[1].ability = None

        game_system.character.append(self.Player(900, 3 * 300 ** (1 / 2), 300 ** (1 / 2), [1, 3, 1, 3, 10]))
        game_system.character[2].xy = [4.5 * w - game_system.character[2].character_width / 2,
                                       19.5 * h,
                                       4.5 * w + game_system.character[2].character_width / 2,
                                       19.5 * h + game_system.character[2].character_height]
        game_system.character[2].identifier = (canvas.create_rectangle(game_system.character[2].xy, fill="white"))
        game_system.character[2].ability = None

        game_system.character.append(self.Player(900, 900 ** (1 / 2), 900 ** (1 / 2), [1.5, 1.5, 1.5, 1.5, 10]))
        game_system.character[3].xy = [7.5 * w - game_system.character[3].character_width / 2,
                                       19.5 * h,
                                       7.5 * w + game_system.character[3].character_width / 2,
                                       19.5 * h + game_system.character[3].character_height]
        game_system.character[3].identifier = (canvas.create_rectangle(game_system.character[3].xy, fill="white"))
        game_system.character[3].ability = "bend_time"

    def __init__(self, battle):
        GameSystem.texture_size = [200, 200]
        self.theme = []
        self.battle = battle
        self.story = []
        self.choices = choices
        self.decisions = []


class GameSystem:

    def resize_canvas(self, event):
        global window_height, window_width, w, h
        GameSystem.pause = True
        window_ratio = window_width / window_height
        self.zoom_ratio = [event.height * window_ratio / window_width, event.height / window_height]
        window_height = event.height
        window_width = event.height * window_ratio
        GameSystem.texture_size = [window_width / 4, window_height / 5]
        canvas.addtag_all("all")
        canvas.config(width=window_width, height=window_height)
        canvas.scale("all", 0, 0, game_system.zoom_ratio[0], game_system.zoom_ratio[1])

        w = window_width / 12
        h = window_height / 30
        self.scale_factor = self.zoom_ratio[1] * window_height / 1000
        self.text_adventure.texture_a, self.text_adventure.texture_b = self.text_adventure.generating_texture(False)
        GameSystem.pause = False

    def activate_keyboard(self):
        canvas.bind("<KeyPress>", self.key_pressed)
        canvas.bind("<KeyRelease>", self.key_released)
        canvas.focus_set()

    def click_event(self, event):
        x = event.x
        y = event.y
        for number in range(len(game_system.character)):
            if game_system.design[number].xy[0] <= x <= game_system.design[number].xy[2] and \
                    game_system.design[number].xy[
                        1] <= y <= \
                    game_system.design[number].xy[3]:
                game_system.player_choice = number
                self.text_adventure.clear_screen()
                self.deactivate_mouse()
                self.activate_keyboard()
                self.battle.move_start_position()

    def key_pressed(self, event):
        if event.keysym == "Left":
            self.battle.direction = "left"
            self.battle.key[0] = 1
        elif event.keysym == "Right":
            self.battle.direction = "right"
            self.battle.key[1] = 1
        elif event.keysym == "Up":
            self.battle.direction = "up"
            self.battle.key[2] = 1
        elif event.keysym == "Down":
            self.battle.direction = "down"
            self.battle.key[3] = 1
        elif event.keysym == "c":
            game_system.cheat = not game_system.cheat
        elif event.keysym == "space":
            game_system.pause = not game_system.pause
            self.battle.enemy_recolor()
        elif event.keysym == "b":
            self.screen_shot = self.boss_key()

    def key_released(self, event):
        if sum(self.battle.key) <= 1:
            self.battle.direction = "0"
        if event.keysym == "Left":
            self.battle.key[0] = 0
        if event.keysym == "Right":
            self.battle.key[1] = 0
        if event.keysym == "Up":
            self.battle.key[2] = 0
        if event.keysym == "Down":
            self.battle.key[3] = 0
        for number in range(4):
            if self.battle.key[number] == 1:
                if number == 0:
                    self.battle.direction = "left"
                elif number == 1:
                    self.battle.direction = "right"
                elif number == 2:
                    self.battle.direction = "up"
                elif number == 3:
                    self.battle.direction = "down"

    def boss_key(self):
        if self.boss == False:
            self.pause = True
            screen_shot = PhotoImage(file="boss_key.png")
            self.boss = canvas.create_image(0, 0, image=screen_shot, anchor=NW)
            self.fullscreen()
            self.deactivate_mouse()
            return screen_shot
        else:
            canvas.delete(self.boss)
            self.pause = False
            self.boss = False
            self.fullscreen()

    def fullscreen(self):
        if (window.attributes('-fullscreen')):
            window.attributes('-fullscreen', False)
        else:
            window.attributes('-fullscreen', True)

    def activate_mouse(self):
        canvas.bind("<Button-1>", self.click_event)

    def deactivate_mouse(self):
        canvas.unbind("<Button-1>")

    @staticmethod
    def deactivate_keyboard():
        canvas.unbind("<Down>")
        canvas.unbind("<Up>")
        canvas.unbind("<Right>")
        canvas.unbind("<Left>")

    def play(self, saved_game):
        self.game_running = True
        self.save_game = saved_game
        if not self.save_game:
            self.text_adventure.clear_screen()
            self.text_adventure.character_boxes()
            self.text_adventure.character_creation()
        elif self.save_game:
            character_save = open("character_saves.txt", "r+")
            character = [line.rstrip("\n") for line in character_save.readlines()]
            character_save.close()

            self.text_adventure.clear_screen()

            self.score = int(character[0])
            self.life = int(character[1])
            self.battle.start_position[0] = float(character[2])
            self.battle.start_position[1] = float(character[3])

            self.player_choice = int(character[5])
            self.level = int(character[6])
            self.text_adventure.character_creation()
            self.deactivate_mouse()
            self.text_adventure.clear_screen()

            self.battle.move_start_position()
            self.battle.life = self.battle.generating_statistic()
            self.text_adventure.texture_a, self.text_adventure.texture_b = self.text_adventure.generating_texture(True)
        return self.battle.generating_statistic(), self.text_adventure.texture_a, self.text_adventure.texture_b

    def check_game_status(self):
        if self.win or self.lose:
            self.game_running = False
            self.text_adventure.clear_screen()
            if self.lose:
                canvas.delete(game_system.character[0].identifier)
                canvas.delete(game_system.level_identifier)
                canvas.delete(game_system.score_identifier)
                for number in range(len(game_system.life_identifier)):
                    canvas.delete(game_system.life_identifier[number])
                game_system.character = []
                self.user_name = self.entry.get()
                if self.user_name == "":
                    self.user_name = "Bob"

                self.leaders[int(self.score)] = self.user_name
                self.leader_list.seek(0, os.SEEK_END)  # find the last line of the file
                self.leader_list.write("\n" + str(self.score) + "\n" + str(self.user_name))
                self.leader_list.close()
                self.leader_list = open("player_records.txt", "r+")

                self.level = 5
                self.game_setup()
                self.menu()

            if self.win:
                self.win = False
                if self.level >= 20:
                    self.lose = True
                    canvas.create_text(6*w,15*h, text="YOU WIN", fill="white", font="times 40 bold italic")
                    time.sleep(5)
                    self.level = 5
                    self.game_setup()
                    self.menu()
                canvas.delete(game_system.character[0].identifier)
                canvas.delete(game_system.level_identifier)
                canvas.delete(game_system.score_identifier)
                game_system.character = []
                for number in range(len(game_system.life_identifier)):
                    canvas.delete(game_system.life_identifier[number])
                self.level = self.level + 1
                self.play(True)
        canvas.after(1000, self.check_game_status)

    def menu(self):
        self.activate_mouse()
        self.text_adventure.texture_a, self.text_adventure.texture_b = self.text_adventure.generating_texture(
            True)

        new_game = Button(text='Begin', command=lambda: self.play(False), font="Times 8")
        saved_game = Button(text='Continue', command=lambda: self.play(True), font="Times 8")

        self.entry = Entry(canvas)

        if self.leaders == {}:
            leaders = [line.rstrip("\n") for line in self.leader_list.readlines()]  # strip line breaks
            for number in range(len(leaders)):
                if number % 2 == 0:
                    leaders[number] = int(leaders[number])
            for number in range(int(len(leaders) / 2)):
                self.leaders[leaders[2 * number]] = leaders[2 * number + 1]
        sorted_values = sorted(self.leaders.keys())

        character_save = open("character_saves.txt", "r+")
        character = [line.rstrip("\n") for line in character_save.readlines()]

        user_name = []
        user_score = []
        count = 0
        if count < len(sorted_values):
            for sorted_key in sorted_values:
                user_name.append(self.leaders[sorted_key])
                user_score.append(sorted_key)
                count += 1
        self.identifier.append(canvas.create_text(10.5 * w, 3 * h, text="F", font="Times 120 italic", fill="black"))
        self.identifier.append(canvas.create_text(7.5 * w, 3 * h, text="D", font="Times 120 italic", fill="white"))
        self.identifier.append(canvas.create_text(4.5 * w, 3 * h, text="S", font="Times 120 italic", fill="black"))
        self.identifier.append(canvas.create_text(1.5 * w, 3 * h, text="A", font="Times 120 italic", fill="white"))
        self.identifier.append(
            canvas.create_text(4.5 * w, 9 * h, text="LEADER", font="Times 20 bold italic", fill="white"))
        self.identifier.append(
            canvas.create_text(7.5 * w, 9 * h, text="BOARD", font="Times 20 bold italic", fill="white"))
        self.identifier.append(
            canvas.create_text(4.5 * w, 14 * h, text="First place", font="Times 15 bold italic", fill="white"))
        self.identifier.append(
            canvas.create_text(7.5 * w, 14 * h, text="Second place", font="Times 15 bold italic", fill="white"))
        self.identifier.append(
            canvas.create_text(4.5 * w, 20 * h, text="Third place", font="Times 15 bold italic", fill="white"))
        self.identifier.append(
            canvas.create_text(7.5 * w, 20 * h, text="Forth place", font="Times 15 bold italic", fill="white"))
        self.identifier.append(
            canvas.create_text(4.5 * w, 15.5 * h, text=str(user_name[-1]) + " " + str(user_score[-1]),
                               font="Times 13 italic", fill="white"))
        self.identifier.append(
            canvas.create_text(7.5 * w, 15.5 * h, text=str(user_name[-2]) + " " + str(user_score[-2]),
                               font="Times 13 italic", fill="white"))
        self.identifier.append(
            canvas.create_text(4.5 * w, 21.5 * h, text=str(user_name[-3]) + " " + str(user_score[-3]),
                               font="Times 13 italic", fill="white"))
        self.identifier.append(
            canvas.create_text(7.5 * w, 21.5 * h, text=str(user_name[-4]) + " " + str(user_score[-4]),
                               font="Times 13 italic", fill="white"))
        self.identifier.append(
            canvas.create_text(4.5 * w, 26 * h, text="And you are", font="Times 15 bold italic", fill="white"))
        self.identifier.append(canvas.create_window(4.5 * w, 27 * h, window=self.entry, height=0.75 * h, width=2 * w))
        self.identifier.append(canvas.create_window(4.5 * w, 28 * h, window=new_game, width=1.5 * w, height=0.75 * h))

        self.identifier.append(
            canvas.create_text(7.5 * w, 26 * h, text="Or you were", font="Times 15 bold italic", fill="white"))
        self.identifier.append(
            canvas.create_text(7.5 * w, 27 * h, text=str(character[4]), font="Times 13 bold italic", fill="white"))
        self.identifier.append(canvas.create_window(7.5 * w, 28 * h, window=saved_game, width=1.5 * w, height=0.75 * h))

    def game_setup(self):
        self.life_identifier = []
        self.player_choice = ""
        self.lose = False
        self.win = False
        self.game_running = False
        self.entry = None
        self.score = 0
        self.difficulty = 1
        self.cheat = False
        self.boss = False
        self.pause = False
        self.life = 5 * self.difficulty
        self.user_name = "BoB"

    def __init__(self, battle, text_adventure):
        self.life_identifier = []
        self.player_choice = ""
        self.save_game = False
        self.lose = False
        self.win = False
        self.game_running = False
        self.entry = None
        self.score = 0
        self.difficulty = 1
        self.level = 1
        self.cheat = False
        self.boss = False
        self.pause = False
        self.life = 10 * self.difficulty
        self.user_name = "BoB"

        self.check_game_status()
        canvas.bind("<Configure>", self.resize_canvas)
        self.leader_list = open("player_records.txt", "r+")
        self.entry = None
        self.leaders = {}
        self.texture_size = [200, 200]
        self.zoom_ratio = [1, 1]
        self.scale_factor = self.zoom_ratio[1] * window_height / 1000
        self.battle = battle
        self.text_adventure = text_adventure
        self.default_size = 900
        self.character = []
        self.xy = [[], []]
        self.design = []
        self.identifier = []
        self.screen_shot = None
        self.activate_keyboard()
        self.menu()


battle = Battle()

text_adventure = TextAdventure(battle)
game_system = GameSystem(battle, text_adventure)
# game_system.text_adventure.image = game_system.text_adventure.generating_story()
# game_system.battle.life = game_system.battle.generating_statistic()
# game_system.text_adventure.texture_a, game_system.text_adventure.texture_b = game_system.text_adventure.generating_texture(
#     True)
# scaling
# main system
# update

window.mainloop()
