class Backgammon:
    bar_white_idx = 0
    bar_black_idx = 25
    START_BOARD = [0, 2, 0, 0, 0, 0, -5, 0, -3, 0, 0, 0, 5, -5, 0, 0, 0, 3, 0, 5, 0, 0, 0, 0, -2, 0]

    def __init__(self, start_board=START_BOARD, white_to_move=True):
        """
        white, positive, white moves to back of list,
        self.board positive is white
        """
        self.board = start_board
        self.white_to_move = white_to_move
        self.white_captured = 0
        self.black_captured = 0
        self.white_to_bar = 0
        self.black_to_bar = 0
        self.white_moves = []  # Список для хранения перемещений белых камней
        self.black_moves = []  # Список для хранения перемещений черных камней
        #self.black_stone_moved = False  # Флаг для отслеживания перемещения черного камня
        #self.white_stone_moved = False  # Флаг для отслеживания перемещения белого камня


    @property #декоратор в Python, который позволяет определить метод класса как свойство, доступное для чтения
    def bar_white(self) -> int:
        return self.board[self.bar_white_idx] 

    @property
    def bar_black(self) -> int:
        return self.board[self.bar_black_idx] #просто для того и того, чтобы обращаться внутри класса а не менять значение снаружи

    @property
    def white_on_bar(self) -> bool:
        return self.bar_white != 0

    @property
    def black_on_bar(self) -> bool: #проверка состояния если не пусто, true и наоборот
        return self.bar_black != 0

    @property
    def white_indices(self) -> list:
        return [i for i, x in enumerate(self.board) if x > 0] #определяем где есть белые шашки, конкретно их места

    @property
    def black_indices(self) -> list:
        return [i for i, x in enumerate(self.board) if x < 0] ##определяем где есть черные шашки, конкретно их места

    @property
    def white_farthest_occupied_point(self) -> int: #выведет самое большое значение(-)
        return min(self.white_indices)

    @property
    def black_farthest_occupied_point(self) -> int: #выведет самое большое значение(+)
        return max(self.black_indices)

    @property #считаем с 0 по 18 позицию есть ли кто-то если 0, то можно выходить с доски
    def white_bearing_off(self) -> bool: 
        count_not_home_board = sum(self.board[i] for i in self.white_indices if self.bar_white_idx <= i <= 18)
        return not bool(count_not_home_board)

    @property #считаем с 25 по 6 позицию есть ли кто-то если 0, то можно выходить с доски
    def black_bearing_off(self) -> bool:
        count_not_home_board = sum(self.board[i] for i in self.black_indices if 7 <= i <= self.bar_black_idx)
        return not bool(count_not_home_board)

    @property #проверяем победил или нет, если список пустой(индексы где есть шашки), то возвращаем True
    def white_won(self) -> bool:
        return not bool(self.white_indices)

    @property
    def black_won(self) -> bool:
        return not bool(self.black_indices)
    
    #def reset_flags(self):  # эти флаги нужны, чтобы не было вывода несколько раз сообщений о введение в бар
        #self.black_stone_moved = False
        #self.white_stone_moved = False