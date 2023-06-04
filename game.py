from board import Backgammon
from dice import roll_die, roll_dice
import random
import json
import os


def prompt_for_input_from_list(options: set): #запрос ответа у пользователя
    response = None
    formatted_options = sorted(options)
    options = {str(x) for x in options}
    while response not in options:
        print("Options: ", formatted_options)
        response = input("Input your selection  -> ")
        if response not in options:
            print("Invalid selection.")
    return response