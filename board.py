class Checker:
    def __init__(self):
        self.white_moves = []  # Список для хранения перемещений белых шашек
        self.black_moves = []  # Список для хранения перемещений черных шашек


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
        self.checker = Checker()
        #self.white_moves = []  # Список для хранения перемещений белых камней
        #self.black_moves = []  # Список для хранения перемещений черных камней
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

    def move(self, start: int, end: int):
        #self.reset_flags()
        if self.white_to_move: #проверка ход ли белых(True да, False чёрные)
            assert self.board[start] > 0, "Invalid move: it is white's turn" #проверка тот ли ходит
            self.board[start] -= 1 #удаление шашки с поля
            if end >= self.bar_black_idx: #уведомление о том, чтобы не идти на бар противника и дальше, выкидывать шашки
                assert self.white_bearing_off, "Invalid move: white is not bearing off" #проверяем условие можно ли выкидывать шашки с поля, если не выполняется то нафиг
            else:
                assert self.board[end] >= -1, "Invalid move: blocked" #проверка, не заблокировано ли место шашками противника
                if self.board[end] == -1: #если там одна шашка, то съедаем и отправляем её в бар
                    self.board[self.bar_black_idx] -= 1
                    self.board[end] = 1
                    self.black_to_bar += 1
                    #if not self.black_stone_moved:
                        #print("The black stone moves to the bar")
                        #self.black_stone_moved = True
                else: #если там не врага, то просто переносим шашку
                    self.board[end] += 1
        else:
            assert self.board[start] < 0, "Invalid move: it is black's turn"
            self.board[start] += 1
            if end <= self.bar_white_idx:
                assert self.black_bearing_off, "Invalid move: black is not bearing off"
            else:
                assert self.board[end] <= 1, "Invalid move: blocked"
                if self.board[end] == 1:
                    self.board[self.bar_white_idx] += 1
                    self.board[end] = -1
                    self.white_to_bar += 1
                    #if not self.white_stone_moved:
                        #print("The white stone moves to the bar")
                        #self.white_stone_moved = True
                    
                else:
                    self.board[end] -= 1

        # Проверка, вышел ли камень из игры для белых ??
        if self.white_to_move and start != self.bar_white_idx and end >= self.bar_black_idx:
            self.white_captured += 1
            print("White stone captured!")

        # Проверка, вышел ли камень из игры для черных
        if not self.white_to_move and start != self.bar_black_idx and end <= self.bar_white_idx:
            self.black_captured += 1
            print("Black stone captured!")

        # Добавляем перемещение в соответствующий список
        if self.white_to_move:
            self.checker.white_moves.append((start, end))
        else:
            self.checker.black_moves.append((start, end))


    def valid_move(self, start: int, end: int) -> bool: #допустимый ли ход в игре
        has_checkers = self.board[start] >= 1 if self.white_to_move else self.board[start] <= -1 #есть ли у игрока, который должен сходить там шашка TRUE если да
        in_range = (self.bar_white_idx < end < self.bar_black_idx) #проверка находится ли end в допустимом значение для перемещения шашки от 1 до 24
        if not in_range: # если не находится доп проверка
            bearing_off = self.white_bearing_off if self.white_to_move else self.black_bearing_off #проверка разрешено ли выносить шашки с доски
            if self.white_to_move:
                valid_bear_off = (end == self.bar_black_idx) or ((end > self.bar_black_idx) and (start == self.white_farthest_occupied_point)) #разрешено ли выносить шашку на позицию end/ Проверяется, больше ли end значения self.bar_black_idx и является ли начальная позиция start самой дальней занятой белой позицией
            else:
                valid_bear_off = (end == self.bar_white_idx) or ((end < self.bar_white_idx) and (start == self.black_farthest_occupied_point))
            return has_checkers and bearing_off and valid_bear_off #идёт проверка по трём условиям
        blocked = self.board[end] <= -2 if self.white_to_move else self.board[end] >= 2 # проверка если находится в диапазоне разрешенного,проверяем не заблокирована ли данная позиция чужой шашкой
        return has_checkers and (not blocked) #итог можно или нет
    

    def generate_valid_moves(self, dice: list) -> list: #варианты допустимых ходов
        #return list of valid (start, end) moves in current position.
        on_bar = self.white_on_bar if self.white_to_move else self.black_on_bar #количество шашек на баре
        bar_index = self.bar_white_idx if self.white_to_move else self.bar_black_idx #сохраняем индекс бара в зависимости от цвета
        possible_start_indices = [bar_index] if on_bar else (self.white_indices if self.white_to_move else self.black_indices) #индексы возможных ходов, если есть что-то на баре, то добавялется оно или наоборот всё остальное
        valid_moves = []
        for die in dice:
            die = die if self.white_to_move else (-die) #если белые то остаётся так как они идут по возвышению,если чёрные то меняем
            valid_moves += [(i, i+die) for i in possible_start_indices if self.valid_move(i, i+die)] #проверка на то возможно ли сделать такой ход, если да, то добавляется в список
        return valid_moves
    
    def generate_valid_turns(self, dice: list) -> list:
        #return list of valid [(start, end), (start, end)] turns in current position.
        def move_die(move): #move кортеж из start and end
            def keep_in_range(index):
                return max(min(index, self.bar_white_idx), self.bar_black_idx) #значение index находится в допустимом диапазоне, про случай нахождения в спец области(бар?)
            return abs(keep_in_range(move[1]) - keep_in_range(move[0])) #возварщение абслютного + значения для вычисления ситуации и значения, в том числе для бара

        def raw_move_die(move):
            return abs(move[1] - move[0]) #сырое значение абсолютное, которое не учитывает состояние на баре

        def sum_dice_turn(turn): #общая сумма расстояний для всех ходов в списке turn
            return sum(move_die(move) for move in turn)

        valid_moves = self.generate_valid_moves(set(dice)) #просто создаётся новый список допустимых ходов, set чтобы оставить только уникальыне значения
        remaining_checkers = abs(sum(self.board[i] for i in (self.white_indices if self.white_to_move else self.black_indices))) #вычисляется количество оставшихся шашек на доске
        if len(dice) == 1 or remaining_checkers == 1: #если 1 кость и 1 шашка то каждый ход из списка valid_moves будет представлен отдельным списком, содержащим только этот ход.
            return [[move] for move in valid_moves]
        valid_turns = [] # все допустимые ходы
        for move in valid_moves:
            remaining_dice = dice[:] #копия костей
            try:
                remaining_dice.remove(raw_move_die(move))
            except ValueError:
                continue # если всё пробрано идём дальше
            copy = self.copy() #если всё норм то копируем настоящее состояние
            copy.move(*move) #здесь вызывается этот метод ход к доске
            if remaining_dice: #проверка остались ли ещё ходы камни
                valid_turns += [[move] + continuation for continuation in copy.generate_valid_turns(remaining_dice)] #рекурсивный вызов метода для копии доски каждое продолжение хода в valid_turns
        if not valid_turns:
            return []
        most_dice = max(len(turn) for turn in valid_turns)
        if most_dice == 1:  # Must play larger die
            larger = max(dice) #1, это означает, что все ходы имеют только один элемент. а затем в valid_turns оставляются только ходы, у которых "сырое" расстояние первого хода (raw_move_die(turn[0])) равно larger.
            valid_turns = [turn for turn in valid_turns if raw_move_die(turn[0]) == larger]
        else:  # Must play most dice possible
            valid_turns = [turn for turn in valid_turns if len(turn) == most_dice] #оставляются только ходы с длиной, равной most_dice
            max_dice_value = max(sum_dice_turn(turn) for turn in valid_turns) #равное максимальной сумме расстояний ходов (sum_dice_turn(turn)) среди всех оставшихся ходов в valid_turns
            valid_turns = [turn for turn in valid_turns if sum_dice_turn(turn) == max_dice_value] #остаются только ходы, у которых сумма расстояний равна max_dice_value.
        return valid_turns #Возвращается список valid_turns с отфильтрованными и отсортированными ходами.


    def copy(self): # для создания копии объекта класса Backgammon.
        return Backgammon(self.board[:], self.white_to_move) #создание копии и внесение тужа доски, второе кто должен сделать ход

    def __str__(self): #принимает целочисленное значение val и возвращает строковое представление этого значения. заменяет цифры на буквы(цвета)
        def tile_to_string(val: int) -> str:
            """ Return three-character string representation """
            if val == 0:
                return "   " #пустота
            if val > 0:
                return f"{val:2d}W" #white
            if val < 0:
                return f"{abs(val):2d}B" #black

        out = " " + "   ".join(f"{x:2d}" for x in range(1, 7))
        out += "   bar   "
        out += "   ".join(f"{x:2d}" for x in range(7, 13))
        out += '\n' + '- ' * 33 + '\n'
        out += '  '.join(tile_to_string(x) for x in self.board[1:7]) + " |"
        out += tile_to_string(self.bar_white) + ' | '
        out += '  '.join(tile_to_string(x) for x in self.board[7:13])
        out += '\n' + '- ' * 33 + '\n'
        out += '  '.join(tile_to_string(x) for x in self.board[24:18:-1]) + " |"
        out += tile_to_string(self.bar_black) + ' | '
        out += '  '.join(tile_to_string(x) for x in self.board[18:12:-1])
        out += '\n' + '- ' * 33 + '\n'
        out += " " + "   ".join(f"{x:2d}" for x in range(24, 18, -1))
        out += "   bar   "
        out += "   ".join(f"{x:2d}" for x in range(18, 12, -1))
        out += "\n"
        out += f"White captured: {self.white_captured}\n"
        out += f"Black captured: {self.black_captured}\n"
        return out


