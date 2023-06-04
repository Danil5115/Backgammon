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

class BackgammonGame(Backgammon): # запуск
    START_BOARD = [0, 2, 0, 0, 0, 0, -5, 0, -3, 0, 0, 0, 5, -5, 0, 0, 0, 3, 0, 5, 0, 0, 0, 0, -2, 0]

    def __init__(self, start_board=START_BOARD, start_new_game=True):
        white_to_move = self.determine_start_player()
        super().__init__(start_board, white_to_move)
        print("""White moving:      Black moving:
    ->->|              <-<-^
    <-<-ˇ              ->->|
    """)
        self.dice = []
        if start_new_game:
            self.turn()

    def save_game(self): #json
        state = {
            "board": self.board,
            "white_to_move": self.white_to_move,
            "dice": self.dice,
            "white captured": self.white_captured,
            "black captured": self.black_captured,
            "white bar count": self.white_to_bar,
            "black bar count": self.black_to_bar,
            "white_moves": self.white_moves,  # Сохраняем список перемещений белых камней
            "black_moves": self.black_moves  # Сохраняем список перемещений черных камней
        }

        with open("game_state.json", "w") as file:
            json.dump(state, file)

    def load_game(self):
        if os.path.exists("game_state.json"):
            with open("game_state.json", "r") as file:
                state = json.load(file)
                self.board = state["board"]
                self.white_to_move = state["white_to_move"]
                self.dice = state["dice"]
                self.white_moves = state["white_moves"]  # Загружаем список перемещений белых камней
                self.black_moves = state["black_moves"]  # Загружаем список перемещений черных камней
        else:
            print("No saved game found.")
        self.turn()

    def determine_start_player(self):
        white_roll = roll_die()
        print("White rolled a", white_roll)
        black_roll = roll_die()
        print("Black rolled a", black_roll)
        if white_roll == black_roll:
            print("Rolling again.")
            return self.determine_start_player()
        elif white_roll > black_roll:
            print("White to play first.")
            return True
        else:
            print("Black to play first.")
            return False

    def roll_and_parse_dice(self):
        dice = roll_dice()
        print("Rolled: ", dice)
        if dice[0] == dice[1]:  # Double
            self.dice = [dice[0]] * 4
        else:
            self.dice = list(dice)