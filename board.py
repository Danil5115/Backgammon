class Checker:
    def __init__(self):
        self.white_moves = []  # List for storing movements of white checkers
        self.black_moves = []  # List for storing movements of black checkers


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
        #self.white_moves = []  # List for storing movements of white stones
        #self.black_moves = []  # List for storing movements of black stones
        #self.black_stone_moved = False  # Flag to track the movement of the black stone
        #self.white_stone_moved = False  # Flag to track the movement of the white stone


    @property 
    def bar_white(self) -> int:
        return self.board[self.bar_white_idx] 

    @property
    def bar_black(self) -> int:
        return self.board[self.bar_black_idx] 

    @property
    def white_on_bar(self) -> bool:
        return self.bar_white != 0

    @property
    def black_on_bar(self) -> bool: 
        return self.bar_black != 0

    @property
    def white_indices(self) -> list:
        return [i for i, x in enumerate(self.board) if x > 0] #we determine where the white checkers are, specifically their places

    @property
    def black_indices(self) -> list:
        return [i for i, x in enumerate(self.board) if x < 0] #we determine where there are black checkers, specifically their places

    @property
    def white_farthest_occupied_point(self) -> int: #will print the largest value(-)
        return min(self.white_indices)

    @property
    def black_farthest_occupied_point(self) -> int: #will print the largest value(+)
        return max(self.black_indices)

    @property #counting from 0 to 18 positions is there anyone, if 0, then you can leave the board
    def white_bearing_off(self) -> bool: 
        count_not_home_board = sum(self.board[i] for i in self.white_indices if self.bar_white_idx <= i <= 18)
        return not bool(count_not_home_board)

    @property #counting from 25th to 6th position is there anyone, if 0, then you can leave the board
    def black_bearing_off(self) -> bool:
        count_not_home_board = sum(self.board[i] for i in self.black_indices if 7 <= i <= self.bar_black_idx)
        return not bool(count_not_home_board)

    @property #check if he won or not, if the list is empty (indices where there are checkers), then return True
    def white_won(self) -> bool:
        return not bool(self.white_indices)

    @property
    def black_won(self) -> bool:
        return not bool(self.black_indices)
    
    #def reset_flags(self):  
        #self.black_stone_moved = False
        #self.white_stone_moved = False

    def move(self, start: int, end: int):
        #self.reset_flags()
        if self.white_to_move: #checking whether white is to move(True yes, False black)
            assert self.board[start] > 0, "Invalid move: it is white's turn" 
            self.board[start] -= 1 #removing a checker from the field
            if end >= self.bar_black_idx: #notification not to go to the opponent's bar and then throw away checkers
                assert self.white_bearing_off, "Invalid move: white is not bearing off" #checking the condition to see if checkers can be thrown out of the field
            else:
                assert self.board[end] >= -1, "Invalid move: blocked" #checking whether the place is blocked by enemy checkers
                if self.board[end] == -1: #if there is one checker, then we eat it and send it to the bar
                    self.board[self.bar_black_idx] -= 1
                    self.board[end] = 1
                    self.black_to_bar += 1
                    #if not self.black_stone_moved:
                        #print("The black stone moves to the bar")
                        #self.black_stone_moved = True
                else: #if there is no enemy there, then we simply move the checker
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

        # Checking if the stone is out of play for White??
        if self.white_to_move and start != self.bar_white_idx and end >= self.bar_black_idx:
            self.white_captured += 1
            print("White stone captured!")

        # Checking if the stone is out of play for Black
        if not self.white_to_move and start != self.bar_black_idx and end <= self.bar_white_idx:
            self.black_captured += 1
            print("Black stone captured!")

        # Add the movement to the corresponding list
        if self.white_to_move:
            self.checker.white_moves.append((start, end))
        else:
            self.checker.black_moves.append((start, end))


    def valid_move(self, start: int, end: int) -> bool: #is this a valid move in the game?
        has_checkers = self.board[start] >= 1 if self.white_to_move else self.board[start] <= -1 #does the player who should move there have a checker TRUE if yes
        in_range = (self.bar_white_idx < end < self.bar_black_idx) #check if end is within a valid value to move the checker from 1 to 24
        if not in_range:
            bearing_off = self.white_bearing_off if self.white_to_move else self.black_bearing_off #checking whether it is allowed to remove checkers from the board
            if self.white_to_move:
                valid_bear_off = (end == self.bar_black_idx) or ((end > self.bar_black_idx) and (start == self.white_farthest_occupied_point)) #is it allowed to move a checker to the position end/ Checks whether end is greater than the value of self.bar_black_idx and whether the initial position start is the furthest occupied white position
            else:
                valid_bear_off = (end == self.bar_white_idx) or ((end < self.bar_white_idx) and (start == self.black_farthest_occupied_point))
            return has_checkers and bearing_off and valid_bear_off #check under three conditions
        blocked = self.board[end] <= -2 if self.white_to_move else self.board[end] >= 2 # check if it is within the allowed range, we check whether this position is blocked by someone else’s checker
        return has_checkers and (not blocked) 
    

    def generate_valid_moves(self, dice: list) -> list: #variants of acceptable moves
        #return list of valid (start, end) moves in current position.
        on_bar = self.white_on_bar if self.white_to_move else self.black_on_bar #number of checkers on the bar
        bar_index = self.bar_white_idx if self.white_to_move else self.bar_black_idx #save the bar index depending on the color
        possible_start_indices = [bar_index] if on_bar else (self.white_indices if self.white_to_move else self.black_indices) #indices of possible moves, if there is something on the bar, then it is added or vice versa everything else
        valid_moves = []
        for die in dice:
            die = die if self.white_to_move else (-die) #if it’s white then it stays as they walk along the hill, if it’s black then we change it
            valid_moves += [(i, i+die) for i in possible_start_indices if self.valid_move(i, i+die)] #checking whether it is possible to make such a move, if so, then it is added to the list
        return valid_moves
    
    def generate_valid_turns(self, dice: list) -> list:
        #return list of valid [(start, end), (start, end)] turns in current position.
        def move_die(move): #move start and end
            def keep_in_range(index):
                return max(min(index, self.bar_white_idx), self.bar_black_idx) #index value is within the acceptable range, about the case of being in a special area (bar?)
            return abs(keep_in_range(move[1]) - keep_in_range(move[0])) #returning an absolute + value to calculate the situation and value, including for the bar

        def raw_move_die(move):
            return abs(move[1] - move[0]) #raw absolute value, which does not take into account the state on the bar

        def sum_dice_turn(turn): #total sum of distances for all moves in the turn list
            return sum(move_die(move) for move in turn)

        valid_moves = self.generate_valid_moves(set(dice)) 
        remaining_checkers = abs(sum(self.board[i] for i in (self.white_indices if self.white_to_move else self.black_indices))) 
        if len(dice) == 1 or remaining_checkers == 1: 
            return [[move] for move in valid_moves]
        valid_turns = [] 
        for move in valid_moves:
            remaining_dice = dice[:] 
            try:
                remaining_dice.remove(raw_move_die(move))
            except ValueError:
                continue 
            copy = self.copy() 
            copy.move(*move) 
            if remaining_dice: 
                valid_turns += [[move] + continuation for continuation in copy.generate_valid_turns(remaining_dice)] #recursively call a method to copy the board each continuation of the move in valid_turns
        if not valid_turns:
            return []
        most_dice = max(len(turn) for turn in valid_turns)
        if most_dice == 1:  # Must play larger die
            larger = max(dice) #1, this means that all moves have only one element. and then in valid_turns only moves are left whose “raw” distance of the first move (raw_move_die(turn[0])) is larger.
            valid_turns = [turn for turn in valid_turns if raw_move_die(turn[0]) == larger]
        else:  # Must play most dice possible
            valid_turns = [turn for turn in valid_turns if len(turn) == most_dice] 
            max_dice_value = max(sum_dice_turn(turn) for turn in valid_turns) 
            valid_turns = [turn for turn in valid_turns if sum_dice_turn(turn) == max_dice_value] 
        return valid_turns #Returns a list of valid_turns with filtered and sorted turns.


    def copy(self): 
        return Backgammon(self.board[:], self.white_to_move) 

    def __str__(self):
        def tile_to_string(val: int) -> str:
            """ Return three-character string representation """
            if val == 0:
                return "   " 
            if val > 0:
                return f"{val:2d}W" 
            if val < 0:
                return f"{abs(val):2d}B" 

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


