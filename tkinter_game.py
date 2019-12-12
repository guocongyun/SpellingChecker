from tkinter import *
from random import *
from PIL import Image, ImageTk

# configuring window
from PIL.Image import ANTIALIAS

window = Tk()
window.title("tkintergame")
screen_width = window.winfo_screenwidth()
screen_height = 1000
print(screen_height)
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
        life = Image.open("pixel_heart.png")
        self.life = ImageTk.PhotoImage(life)
        # life = life.resize((int(GameSystem.texture_size[0]), int(GameSystem.texture_size[1])), Image.ANTIALIAS)
        # life = ImageTk.PhotoImage(self.life)
        game_system.life_identifier = []
        for number in range(game_system.life):
            game_system.life_identifier.append(
                canvas.tag_raise(canvas.create_image(h + number * 30, h, image=self.life, anchor=NW)))

        text = "Score : " + str(game_system.score)
        game_system.score_identifier = canvas.create_text(window_width - 100, h, fill="white", font="Times 10 bold",
                                                          text=text, anchor=NW)

        return self.life

    def move_start_position(self):
        self.position = canvas.coords(game_system.character[0].identifier)
        if self.position[0] < 6 * w - game_system.character[0].character_width / 2 - 2:
            canvas.move(game_system.character[0].identifier, 1, 0)
            canvas.after(5, self.move_start_position)
        elif self.position[0] > 6 * w - game_system.character[0].character_width / 2 + 2:
            canvas.move(game_system.character[0].identifier, -1, 0)
            canvas.after(5, self.move_start_position)
        elif self.position[1] < 30 * h - game_system.character[0].character_height - 2:
            canvas.move(game_system.character[0].identifier, 0, 1)
            canvas.after(5, self.move_start_position)
        elif self.position[1] > 30 * h - game_system.character[0].character_height + 2:
            canvas.move(game_system.character[0].identifier, 0, -1)
            canvas.after(5, self.move_start_position)
        else:
            self.character_movement()
            self.enemy_creation()
            self.enemy_movement()
            self.character_ability()

    class normal_enemy:

        # def character_width(self):
        #     character_width = self.character_size ** (1 / 2)
        #     return character_width
        #
        # def character_height(self):
        #     character_height = self.character_size ** (1 / 2)
        #     return character_height

        def __init__(self, character_size):
            self.character_attribute = [1, 1, 3]
            self.character_height = character_size ** (1 / 2)
            self.character_width = character_size ** (1 / 2)
            self.character_size = character_size

    # class weak_enemy(normal_enemy):
    #     def __init__(self):
    #         super().__init__()
    #         self.character_size = GameSystem.character[0].character_width * GameSystem.character[0].character_height - 100

    def enemy_creation(self):
        number_of_enemy = game_system.level  # randint(2,20)
        weak_enemy = 1 + int(number_of_enemy / 10)
        enemy_count = 0
        while enemy_count < number_of_enemy:
            overlap = False
            if enemy_count < weak_enemy:
                character_size = (game_system.character[0].character_width * game_system.character[
                    0].character_height - 100) * game_system.scale_factor
                color = "yellow"
            else:
                character_size = (game_system.character[0].character_width * game_system.character[
                    0].character_height + 100 * (enemy_count - weak_enemy)) * game_system.scale_factor
                color = "#cc" + str(99 - int(85 / (number_of_enemy - weak_enemy)) * enemy_count) + "ff"
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
                # GameSystem.characters.append(canvas.create_rectangle(GameSystem.xy[1][enemy_count + 1], fill=color))
                # GameSystem.xy[1].append(enemy_position)
                # GameSystem.characters.append(canvas.create_rectangle(GameSystem.xy[1][enemy_count + 1], fill=color))
                # GameSystem.character_size.append(
                #     [GameSystem.character[enemy_count].character_width, GameSystem.character[enemy_count].character_height])
                # GameSystem.character_attribute.append(GameSystem.character[enemy_count])
                enemy_count += 1

    def character_growth(self):
        game_system.score = game_system.score + 10
        canvas.delete(game_system.score_identifier)
        self.generating_statistic()
        game_system.character[0].character_size = game_system.character[
                                                      0].character_size * game_system.scale_factor + 100 * game_system.difficulty * game_system.scale_factor
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
        position = canvas.coords(game_system.character[0].identifier)
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
        for character_i in range(len(game_system.character) - 1):
            character_i = character_i + 1 - removed_character
            count = 1
            position_i = canvas.coords(game_system.character[character_i].identifier)
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
                            # if position_j[0] <= position_i[0] < position_j[2] or position_j[0] <= position_i[2] < position_j[2]:
                            #     if position_j[1] <= position_i[1] < position_j[3] or position_j[1] <= position_i[3] < position_j[3]:\
                            # counts[character_i] += 1
                            count += 1
                            if count <= 1:
                                game_system.character[character_i].character_attribute[0] = - \
                                    game_system.character[character_i].character_attribute[0]
                                game_system.character[character_i].character_attribute[1] = - \
                                    game_system.character[character_i].character_attribute[1]

    def lose_life(self):
        game_system.life = game_system.life - 1
        for number in range(len(game_system.life_identifier)):
            canvas.delete(game_system.life_identifier[number])
        canvas.delete(game_system.score_identifier)
        self.life = self.generating_statistic()
        if game_system.life == 0:
            canvas.create_text(6 * w, 15 * h, fill="white", font="Times 30 bold", text="YOU LOSE", anchor=CENTER)

    def character_movement(self):
        if not game_system.pause:
            self.check_character_boarder()
            if self.direction == "left":
                canvas.move(game_system.character[0].identifier,
                            game_system.scale_factor * self.collide[0] * -game_system.character[0].character_attribute[
                                1], 0)
            elif self.direction == "right":
                canvas.move(game_system.character[0].identifier,
                            game_system.scale_factor * self.collide[1] * game_system.character[0].character_attribute[
                                3], 0)
            elif self.direction == "up":
                canvas.move(game_system.character[0].identifier, 0,
                            game_system.scale_factor * self.collide[2] * -game_system.character[0].character_attribute[
                                0])
            elif self.direction == "down":
                canvas.move(game_system.character[0].identifier, 0,
                            game_system.scale_factor * self.collide[3] * game_system.character[0].character_attribute[
                                2])
                # repeat movement
            self.collide = [1, 1, 1, 1]
        canvas.after(game_system.character[0].character_attribute[4], self.character_movement)

    def enemy_movement(self):
        self.check_enemy_boarder()
        print(game_system.scale_factor)
        if not game_system.pause and self.ability != "stop":
            for character in range(len(game_system.character) - 1):
                enemy = character + 1
                canvas.move(game_system.character[enemy].identifier,
                            game_system.scale_factor * game_system.character[enemy].character_attribute[0],
                            game_system.scale_factor * game_system.character[enemy].character_attribute[1])

        canvas.after(game_system.character[1].character_attribute[2], self.enemy_movement)

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
        self.texture_a = ImageTk.PhotoImage(self.texture_a)
        self.texture_b = ImageTk.PhotoImage(self.texture_b)
        count = 0
        for number in range(int(window_height / GameSystem.texture_size[1])):

            # print(int(window_width / GameSystem.texture_size[0]))
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
        try:
            canvas.delete(game_system.image_identifier)
            canvas.delete(game_system.story_identifier)
        except:
            pass
        # image = Image.open(self.image_file)
        # image = image.subsample(3)
        # game_system.image_identifier = (canvas.create_image(h, h, image=image, anchor=NW))
        game_system.story_identifier = (canvas.create_text(window_width / 2 + h, h, fill="white", font="Times 10 bold",
                                                           text=self.text, anchor=NW))
        # return image

    # def generate_decisions(self):
    #     # choice 4 Box choices
    #     for i in range(4):
    #         if i < 2:
    #             GameSystem.xy[0].append(
    #                 [2 * w + i * 4 * w, 9 * h, 2 * w + (i + 1) * 4 * w,
    #                  10 * h])
    #             self.decisions.append(canvas.create_rectangle(GameSystem.xy[0][i], fill="grey", outline='black'))
    #             self.decisions.append(
    #                 canvas.create_text(w * 4 + i * w * 4, h / 2 + 9 * h,
    #                                    fill="white",
    #                                    font="Times 10", text=self.choices[i]))
    #         else:
    #             GameSystem.xy[0].append(
    #                 [2 * w + (i - 2) * 4 * w, 10 * h, 2 * w + (i - 1) * 4 * w,
    #                  11 * h])
    #             self.decisions.append(canvas.create_rectangle(GameSystem.xy[0][i], fill="grey", outline='black'))
    #             self.decisions.append(
    #                 canvas.create_text(w * 4 + (i - 2) * w * 4, h / 2 + 10 * h,
    #                                    fill="white",
    #                                    font="Times 10", text=self.choices[i]))

    def clear_screen(self):
        for number in range(len(game_system.design)):
            canvas.delete(game_system.design[number].identifier)
            canvas.delete(game_system.design[number].identifier_text)
        for number in range(len(game_system.character)):
            if number != game_system.player_choice:
                canvas.delete(game_system.character[number].identifier)
        game_system.character = [game_system.character[game_system.player_choice]]

    def light_area(self, list, option):
        canvas.itemconfigure(list[option], fill="red")

    def dim_area(self, list, option):
        canvas.itemconfigure(list[option], fill="grey")

    def click_event(self, event):
        x = event.x
        y = event.y
        history = []
        for number in range(len(game_system.xy[0])):
            if game_system.design[number].xy[0] <= x <= game_system.design[number].xy[2] and \
                    game_system.design[number].xy[
                        1] <= y <= game_system.design[number].xy[3]:
                self.light_area(TextAdventure.decisions, number)
                canvas.after(500, self.dim_area, TextAdventure.decisions, number)

                self.clear_screen(number)
                self.deactivate_mouse()
                self.battle.move_start_position()

    def __init__(self, battle, image_file, text, choices):
        self.theme = []
        self.battle = battle
        self.image_file = image_file
        self.text = text
        self.story = []
        self.choices = choices
        self.decisions = []


class Tutorial(TextAdventure):
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

    def generating_story(self):
        try:
            for number in range(len(game_system.design)):
                canvas.delete(game_system.design[number].identifier)
                canvas.delete(game_system.design[number].identifier_text)
                game_system.design = []
        except:
            pass
        try:
            for number in range(len(game_system.character)):
                canvas.delete(game_system.character[number].identifier)
                game_system.character = []
        except:
            pass
        self.character_boxes()
        self.character_creation()
        return super().generating_story()

    def __init__(self, battle, image_file, text, choices):
        super().__init__(battle, image_file, text, choices)

        GameSystem.texture_size = [200, 200]


class GameSystem:

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
                self.text_adventure.battle.move_start_position()

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
            self.enemy_recolor()
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

    def selecting(self):
        self.text_adventure.image = self.text_adventure.generating_story()
        self.battle.life = self.battle.generating_statistic()
        self.text_adventure.texture_a, self.text_adventure.texture_b = self.text_adventure.generating_texture(
            True)

    def menu(self):
        self.text_adventure.texture_a, self.text_adventure.texture_b = self.text_adventure.generating_texture(
            True)

    def __init__(self, battle, text_adventure):
        self.texture_size = [200, 200]
        self.zoom_ratio = [1, 1]
        self.scale_factor = self.zoom_ratio[1] * window_height / 1000
        self.battle = battle
        self.text_adventure = text_adventure
        self.score = 0
        self.default_size = 900
        self.difficulty = 1
        self.level = 25
        self.character = []
        self.xy = [[], []]
        self.design = []
        self.cheat = False
        self.life = 100 * self.difficulty
        self.screen_shot = None
        self.boss = False
        self.pause = False
        # self.deactivate_mouse()
        self.activate_keyboard()
        self.activate_mouse()
        # self.deactivate_keyboard()
        # self.menu()


battle = Battle()

image_file = "forest.png"
text = "Please select your character"
choices = ["Please choose a character", "Please choose a character", "Please choose a character",
           "Please choose a character"]

textadventure = Tutorial(battle, image_file, text, choices)
game_system = GameSystem(battle, textadventure)
game_system.text_adventure.image = game_system.text_adventure.generating_story()
game_system.battle.life = game_system.battle.generating_statistic()
game_system.text_adventure.texture_a, game_system.text_adventure.texture_b = game_system.text_adventure.generating_texture(
    True)
# scaling
# main system
# update

window.mainloop()
