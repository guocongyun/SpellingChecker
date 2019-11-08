import datetime
import os
import re
import textwrap
from difflib import SequenceMatcher
from ttictoc import TicToc
import time

lines = os.get_terminal_size().lines  # get the terminal height
columns = os.get_terminal_size().columns  # get the terminal width

# Please use a IDE that support terminals and don't change the terminal size when running the program
# throughout the file, i frequently uses + " " + to add spaces , and uses , " " , to change the line 

# this is function for printing the boarder, where print_lines is the line printed
# feed_back is whether to wait for 0.5 for user to read the feed back
# and title is the title of the current menu
def format(print_lines, feed_back,title):
    os.system("clear")

    print("\u250F", end="")  # top left corner
    for item in range(0, columns - 2):  # top border
        print("\u2501", end="")
    print("\u2513", end="")  # top right corner

    print("\u2503", " " * (columns - 4), "\u2503", end="")
    print("\u2503" + title + " " * (columns - 2 - len(title)) + "\u2503", end="")  # print the title

    count = 0
    while count < len(print_lines):  # the while loop print out the strings in print_lines variable
        print("\n\u2503", print_lines[count], " " * (columns - 5 - len(print_lines[count])), "\u2503",
              end="")  # concatonate the strings with the left and right side format
        count += 1
    while count < (
            lines - 5):  # function will printing out left and right side format until terminal height is reached
        print("\n\u2503", " " * (columns - 4), "\u2503", end="")
        count += 1

    print("\u2517", end="")  # bottom left corner
    for item in range(1, columns - 1):  # bottom border
        print("\u2501", end="")
    print("\u251B", end="")  # bottom right corner
    if feed_back == True:
        time.sleep(0.3) # allow user to  have time to see the feed back


# this is a function for checking if the user inputted word is correct
def checking_spelling(user_sentence):
    english_words_file = open("EnglishWords.txt", "r+")
    english_words = [line.rstrip("\n") for line in english_words_file.readlines()]  # strip line breaks
    lower_case_user_sentence = user_sentence.lower()  # change the user sentence into lower cased
    strip_user_sentence = re.sub("[^a-zA-Z]+", " ", lower_case_user_sentence)  # strip non Alpha characters
    strip_user_sentence = strip_user_sentence.strip()  # strip blank spaces in beginning and end
    split_user_sentence = strip_user_sentence.split(" ")  # split the sentence
    spell_check_statistics = {
        "number_of_words": 0,
        "number_of_correct_words": 0,
        "number_of_incorrect_words": 0,
        "number_of_ignored_words": 0,
        "number_of_added_words": 0,
        "number_of_changed_words": 0,
    }

    for item in split_user_sentence:
        spell_check_statistics["number_of_words"] += 1

        if item in english_words:
            spell_check_statistics["number_of_correct_words"] += 1  # count the number of correct words
            feed_back = [" ",
                         "In your sentence,  [" + item + "] spelt correctly"]
            format(feed_back, True, "  W O R D   S P E L T   C O R R E C T L Y")

        else:
            feed_back = [" ",
                         "In your sentence,  [" + item + "] not found in dictionary",
                         " ",
                         "Please wait while checking for similar words...",
                         ]
            format(feed_back, False, "  W O R D   N O T   F O U N D")
            similarity = [0, "words"]
            # loop through the english words to check the similarity between input andividual words
            for words in english_words:
                new_key = SequenceMatcher(a=item, b=words).ratio()
                if new_key > similarity[0]:
                    similarity = [new_key, words]
            del feed_back[-1]
            new_word_sorted = False
            while not new_word_sorted:
                print_lines = feed_back + ["Did you mean [" + similarity[1] + "] ?"]
                format(print_lines, False, "  W O R D   N O T   F O U N D")
                change_word = input("\u2517" + "\u2501" * 5 + " Enter [y] or [n]: ").lower()

                if change_word == "y":
                    symbol = ""
                    feed_back = [" ", "Congratualtion, you have successfully changed the word"]
                    item = similarity[1]
                    spell_check_statistics["number_of_changed_words"] += 1  # count the number of added words

                else:
                    print_lines = [" ",
                                   item,
                                   " ",
                                   "Enter[I]. to [Ignore] the word ", " ",
                                   "Enter[M]. to [Mark] the word as incorrect", " ",
                                   "Enter[A]. to [Add] the word to dictionary",
                                   " "]
                    format(print_lines, False, "  W O R D   N O T   F O U N D")
                    ignore_mark_add = input("\u2517" + "\u2501" * 5 + " Enter choice: ").lower()

                    if ignore_mark_add == "i":
                        symbol = "!"
                        feed_back = [" ", "Congratualtion, you have successfully ignored the word"]
                        spell_check_statistics["number_of_ignored_words"] += 1  # count the number of ignored words

                    elif ignore_mark_add == "m":
                        symbol = "?"
                        feed_back = [" ", "Congratualtion, you have successfully marked the word"]
                        spell_check_statistics["number_of_incorrect_words"] += 1  # count the number of incorrect words

                    elif ignore_mark_add == "a":
                        english_words_file.seek(0, os.SEEK_END)  # find the last line of the file
                        english_words_file.write("\n" + item)  # add the new word to the english word file
                        symbol = "*"
                        feed_back = [" ", "Congratualtion, you have successfully added the word"]
                        spell_check_statistics["number_of_added_words"] += 1  # count the number of added words

                    else:  # if entered anything else, the program will ask the user to enter the option again
                        feed_back = ["Your choice is not one of the options"]
                        # if  entered "[i]", "[m]"... user will get a different feed back
                        if len(ignore_mark_add) != 1:
                            feed_back = [" ", "Please only enter a one letter"]
                        feed_back = print_lines + feed_back
                        format(feed_back, True, "  E R O R R   M E S S A G E")
                        continue
                feed_back = print_lines + feed_back  # print out the feed back line
                format(feed_back, True, "  C H A N G I N G   W O R D")
                unknown_word = symbol + item + symbol  # mark ignored, marked, added symbol around the unknown word
                # replace the original word with the "marked" word
                split_user_sentence[spell_check_statistics["number_of_words"] - 1] = unknown_word
                new_word_sorted = True  # allow user to exit the loop
    joined_user_sentence = " " + " ".join(split_user_sentence)
    # wrap the new user sentence to fit the terminal width and make it neater
    new_user_sentence = textwrap.wrap(joined_user_sentence,width=columns - 6)
    english_words_file.close()  # closing the file
    return spell_check_statistics, new_user_sentence


# this is a function for formulating the statistics and writing the output report
def spell_check_result(option):  # this function format the output spelling report
    spell_check_report = [" ",
                          " Datetime: " + str(datetime.datetime.now().replace(microsecond=0)),
                          # add the date to the spelling report
                          " ",
                          " Number of total words: " + str(spell_check_statistics["number_of_words"]), " ",
                          " Number of correct words: " + str(spell_check_statistics["number_of_correct_words"]), " ",
                          " Number of incorrect words: " + str(spell_check_statistics["number_of_incorrect_words"]),
                          " ",
                          " Number of ignored words: " + str(spell_check_statistics["number_of_ignored_words"]), " ",
                          " Number of added words: " + str(spell_check_statistics["number_of_added_words"]), " ",
                          " Number of changed words: " + str(spell_check_statistics["number_of_changed_words"]), " ",
                          " The sentences you checked: ",
                          " ",
                          " "
                          ] + new_user_sentence + [  # + is used since new_user_sentence variable is a list
                          " ",
                         ]

    if option == "f":  # the function will write the spelling report in the new file, if option is file
        for item in spell_check_report:
            item = item + "\n"  # the function will change line, i.e. by adding "\n", at the end of every line
            file.write(item)
    return spell_check_report


# this is the main spell checking program that uses the three functions
continue_check_spelling = True
while continue_check_spelling:
    time_recorded = TicToc()  # using time_recorded function to count the time
    time_recorded.tic()  # start timing
    print_lines = [" ",
                   " Enter[F]. to check a [File] ", " ",
                   " Enter[S]. to check a [Sentence] ", " ",
                   " ",
                   " Enter anything else to quit ",
                   " ",
                   ]
    format(print_lines, False, "  S P E L L   C H E C K E R")
    option = input("\u2517" + "\u2501" * 5 + " Enter choice: ").lower()

    # If user entered "File", "Sentence", "[F]" or "S" that have f or s in it they are allow to enter the option again
    if len(option) != 1:
        if "f" in option or "s" in option:
            feed_back = [" Please only enter a one letter"]
            print_lines = print_lines + feed_back
            format(feed_back, True, "  E R R O R   M E S S A G E")
            continue

    # if the user enter anything that doesn't countain f or s, they will quit the program
    if option != "f" and option != "s":
        print_lines = [" ",
                       " Have a nice day!",
                       " ",
                       " You have quited the spell check program"]
        format(print_lines, False, "  T H A N K   Y O U   F O R   Y O U R   T I M E !")
        exit()

    elif option == "f":
        print_lines = [" ",
                       " Please enter the file name, then press [Enter]"]
        format(print_lines, False, "  L O A D I N G   F I L E")
        file_name = input("\u2517" + "\u2501" * 5 + " File name: ")
        if os.path.exists(file_name):  # check if the user file name exists
            user_file = open(file_name, "r")
            user_sentence = user_file.read().replace("\n", " ")
        else:
            feed_back = [" ", " Please check if the file exists", " ", " Returning to the menu page..."]
            print_lines = print_lines + feed_back
            format(feed_back, True, "  E R R O R   M E S S A G E")
            continue
        print_lines = [" ",
                       " Please enter the spelling report name, then press [Enter]",
                       " ",
                       " (Or press enter without entering anything to use the default name)"]
        format(print_lines, False, "  E N T E R I N G   F I L E   N A M E")
        spelling_report_name = input("\u2517" + "\u2501" * 5 + " Spelling report name ")
        spell_check_statistics, new_user_sentence = checking_spelling(user_sentence)
        if spelling_report_name == "":
            file_name = file_name.replace(".txt", "")
            # the new file have the default name of the original file + spell_checked
            file = open(file_name + " spelling_report.txt","w")
        else:
            file = open(spelling_report_name + ".txt", "w")
        # the parameter is the option variable, f stend for spell check file
        spell_check_report = spell_check_result("f")
        file.close()  # closing the file

    elif option == "s":
        print_lines = [" ",
                       " Please enter the sentence, then press [Enter]"]
        format(print_lines, False, "  E N T E R   S E N T E N C E")
        user_sentence = input("\u2517" + "\u2501" * 5 + " Sentence: ")  # ask user to input a snce
        spell_check_statistics, new_user_sentence = checking_spelling(user_sentence)
        # the parameter is the option variable, s stand for spell check sentence
        spell_check_report = spell_check_result("s")

    time_recorded.toc()  # end timing
    # add the time elapsed to the spelling report
    print_lines = spell_check_report + [" " + str(time_recorded.elapsed)[:6] + "... seconds used"," "]
    format(print_lines, False, "  S P E L L I N G   R E P O R T")  # the function will print out the spelling report
    continue_check_spelling = bool(
        "" == input("\u2517" + "\u2501" * 5 + " Please press Enter to continue or press any other key to exit "))
