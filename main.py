from game import BackgammonGame

def prompt_for_input():
    print("Options:")
    print("1. Start a new game")
    print("2. Continue the last saved game")
    print("3. Exit")
    return input("Input your selection -> ")

choice = prompt_for_input()
if choice == "1":
    game = BackgammonGame()
elif choice == "2":
    game = BackgammonGame(start_new_game=False)
    game.load_game()  # Загрузка сохраненного состояния игры
elif choice == "3":
    print("Goodbye!")
else:
    print("Invalid selection.")
