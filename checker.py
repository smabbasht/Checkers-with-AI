import os
import random
from typing import Optional


class Checker:
    """class to simulate checkers game where computer play against computer"""
    L1_norm = lambda x, y: abs(x[0] - y[0]) + abs(x[1] - y[
        1])  # gives the distance in L_1 space
    normal_unit_hops = {(1, 1), (-1, -1), (1, -1),
                        (-1, 1)}  # normal unit hopes
    count = {'b': 24, 'w': 24}  # count of the pieces
    tile = {
        'b': '⚫',
        'B': '⬛',
        'w': '⚪',
        'W': '⬜',
        'r': '🟥',
        'y': '🟨',
        'h': '🟩'
    }  # tiles used to print the board

    def __init__(self, human: bool = False, clear_screen: bool = True) -> None:
        """Constructor

        Args: 
            clear_screen (bool, optional): if True then clear screen after each new move. Defaults to True.
        """
        self.human = human
        self.clear_screen = clear_screen
        self.last_move = set()  # set that contain all the last move piece had
        self.initiate_pieces()  # places the pieces on the board
        # parity to avoid the color segeration
        self.parity = {'w': {0: True, 1: True}, 'b': {0: True, 1: True}}

    def initiate_pieces(self) -> None:
        """places the pieces on the board"""
        self.piece = dict()
        for c in range(8):
            for r in range(3):
                self.piece[(
                    r, c
                )] = 'b'  # placing the black pieces on the upper three rows of the board
            for r in range(3, 5):
                self.piece[(
                    r, c
                )] = 'o'  # placing the empty pieces on the mid two rows of the board
            for r in range(5, 8):
                self.piece[(
                    r, c
                )] = 'w'  # placing the white pieces on the lower three rows of the board

    def print_board(self) -> None:
        """print the board on the terminal"""
        if self.clear_screen:
            os.system('clear')
        print('  ', end=' ')
        for i in range(8):
            print(i, end='  ')
        print()
        # color = 'r'  # color for alternating tiles
        for i in range(8):
            print(i, end='  ')
            for j in range(7):
                color = 'y' if (i + j) % 2 else 'r'  # changing the color
                p = 'h' if (i, j) in self.last_move else self.piece[(
                    i, j
                )]  # if piece was in the last move then its 'h' for tiling
                if p == 'o':
                    p = color  # color for empty piece
                print(self.tile[p], end=' ')

            # repeating the same thing just to avoid printing the next
            # row in the very same line because of end=''

            color = 'y' if (i + 7) % 2 else 'r'
            p = 'h' if (i, 7) in self.last_move else self.piece[(i, 7)]
            if p == 'o':
                p = color

            print(self.tile[p])

    def move(self, pos: Optional[tuple[int, int]], side: str) -> None:
        """moves the piece according to the sequence of position given to

        Args:
            pos (Optional[tuple[int, int]]): sequence of position to move piece on the board
            side (str): piece is from which side
        """

        self.last_move = set()  # clearing the last move
        opp_side = 'b' if side == 'w' else 'w'  # changing the sides
        # function to calculate mid of two position
        mid_rc = lambda x, y: ((x[0] + y[0]) >> 1, (x[1] + y[1]) >> 1)

        # if the are only two hops and they are trivial means only
        # hoping to their digonally adjacent neighbours
        if len(pos) == 2 and Checker.L1_norm(pos[0], pos[1]) == 2:
            self.piece[pos[1]] = self.piece[pos[0]].upper(
            ) if pos[1][0] == 7 * (side == 'b') else self.piece[pos[0]]

            self.piece[pos[0]] = 'o'
            self.last_move = {pos[0]}

        else:
            # if the hop is beating the opposite side pieces
            for i in range(len(pos) - 1):
                if (  # there is always an empty piece after the hop
                        self.piece[pos[i + 1]] == 'o'
                        # the hop must be jumping two squares doiagonally
                        and Checker.L1_norm(pos[i + 1], pos[i]) == 4
                        # there must be a peice of opposite side between the jump and landing position
                        and self.piece[mid_rc(pos[i + 1], pos[i])].lower()
                        == opp_side):

                    self.count[opp_side] -= 1  # reducing the count
                    # setting the middle piece as empty piece
                    self.piece[mid_rc(pos[i + 1], pos[i])] = 'o'

                    # checking if horse has to be made
                    if pos[i + 1][0] == 7 * (side == 'b'):
                        self.piece[pos[i + 1]] = self.piece[pos[i]].upper()
                    else:
                        self.piece[pos[i + 1]] = self.piece[pos[i]]

                    self.piece[pos[i]] = 'o'  # setting middle as empty
                    self.last_move.add(pos[i])  # updating the last move
                else:
                    # breaking the chain of hopping because we have illegal hops from now
                    break

    @staticmethod
    def direction(dr: int, dc: int) -> str:
        """returns the direction in which the change is happening

        Args:
            dr (int): change in row
            dc (int): change in column

        Returns:
            str: the direction string
        """
        return ('dl' * (dc < 0) + 'dr' *
                (dc > 0)) * (dr > 0) + ('ul' * (dc < 0) + 'ur' *
                                        (dc > 0)) * (dr < 0)

    def hops(self,
             r: int,
             c: int,
             path: dict = dict(),
             visited: set = set(),
             first: bool = True) -> dict:
        """returns all the hops than can happen from a given position.

        Args:
            r (int): row of the piece
            c (int): column of the piece
            path (dict, optional): container storing the path. Defaults to dict().
            visited (set, optional): visited position. Defaults to set().
            first (bool, optional): True if the hop is first hop. Defaults to True.

        Returns:
            dict: container that contains all the paths
        """

        p = self.piece[(r, c)]
        # allowed hops and the pieces to hop on
        if p == 'b':
            hops = {(1, 1), (1, -1)}
            allowed = {'w'}
        elif p == 'w':
            hops = {(-1, 1), (-1, -1)}
            allowed = {'b'}
        else:
            hops = self.normal_unit_hops
            if p == 'B':
                allowed = {'w', 'W'}
            else:
                allowed = {'b', 'B'}

        path['coordinate'] = (r, c)  # adding the coordinates

        for d in {'ur', 'ul', 'dr', 'dl'}:
            path[d] = path.get(d, None)  # to avoid any error

        # if it is our first hop only then we can hop onto your diagonal neighbours
        if first:
            for dr, dc in hops:
                r_ = r + dr  # r' = r + Δr
                c_ = c + dc  # c' = c + Δc
                if 0 <= r_ < 8 and 0 <= c_ < 8 and self.piece[(r_, c_)] == 'o':
                    path[self.direction(dr, dc)] = {
                        'coordinate': (r_, c_),
                        'ur': None,
                        'ul': None,
                        'dr': None,
                        'dl': None
                    }

        for dr, dc in hops:
            r_ = r + 2 * dr  # r' = r + 2 * Δr
            c_ = c + 2 * dc  # c' = c + 2 * Δc
            if (0 <= r_ < 8 and 0 <= c_ < 8 and (r_, c_) not in visited
                    and self.piece[(r + dr, c + dc)] in allowed
                    and self.piece[(r_, c_)] == 'o'):
                path[self.direction(dr, dc)] = {
                    'coordinate': (r_, c_),
                    'ur': None,
                    'ul': None,
                    'dr': None,
                    'dl': None
                }
                visited.add((r_, c_))  # visiting the position
                # exploring more hops
                self.hops(r_, c_, path[self.direction(dr, dc)], visited, False)
        return path

    def deepest_path(self, path: dict) -> Optional[tuple]:
        """returns the deepest path in a tree, if there are more 
        than one then select any one randomly

        Args:
            path (dict): tree in a form of nested dictionaries

        Returns:
            Optional[tuple]: list of all nodes that are on the 
            deepest path in the tree
        """
        # if there is no way to go more
        if path is None:
            return []

        # exploring path in down right direction
        down_right = self.deepest_path(path['dr'])
        # exploring path in down left direction
        down_left = self.deepest_path(path['dl'])
        # exploring path in up right direction
        up_right = self.deepest_path(path['ur'])
        # exploring path in up left direction
        up_left = self.deepest_path(path['ul'])

        length = [len(down_right), len(down_left), len(up_right), len(up_left)]
        deepest = max(length)

        if length[0] == deepest:
            down_right.append(path['coordinate'])
        if length[1] == deepest:
            down_left.append(path['coordinate'])
        if length[2] == deepest:
            up_right.append(path['coordinate'])
        if length[3] == deepest:
            up_left.append(path['coordinate'])

        # randomly chossing a path from all path

        index = [0, 1, 2, 3]
        i = random.choice(index)

        while length[i] != deepest:
            index.remove(i)
            i = random.choice(index)

        if i == 0:
            return down_right
        if i == 1:
            return down_left
        if i == 2:
            return up_right
        if i == 3:
            return up_left

    def paths(self, side: str) -> Optional[Optional[tuple[int, int]]]:
        """returns the deepest path of all pieces from side

        Args:
            side (str): the side to find the deepest path of its pieces

        Returns:
            Optional[Optional[tuple[int,int]]]: list of a deepest 
            path possible for each piece"""
        path = []  # container for all deepest paths from all position
        side_parity = {0: False, 1: False}  # setting parity false for new run
        for r in range(8):
            for c in range(8):
                if self.piece[(r, c)].lower() == side:
                    # updating the parity
                    side_parity[(r + c) % 2] = side_parity[(r + c) % 2] or True
                    # appending the deepest path in the path container
                    path.append(self.deepest_path(self.hops(r, c)))
        self.parity[side] = side_parity  # setting the parity
        return path

    def human_move(self) -> Optional[tuple[int, int]]:
        """collects the move human wants to play

        Returns:
            Optional[tuple[int, int]]: list of moves from human
        """
        print('Enter your move dear human.')
        cin = input()  # taking inpurt from human
        pos = (int(cin[0]), int(cin[2]))
        move = [pos]
        while True:
            # if human gives q then stops the input and return the collected moves
            cin = input()
            if cin == 'q':
                break
            pos = (int(cin[0]), int(cin[2]))
            move.append(pos)
        return move

    def computer_move(self, side: str) -> Optional[tuple[int, int]]:
        """returns the move computer wanna play

        Args:
            side (str): side which computer playing

        Returns:
            Optional[tuple[int, int]]: list of the position to 
            move piece on the board"""
        path = self.paths(side)
        moves = {}  # dict for all moves
        jump = 0  # depth of the hop
        for k in path:
            if len(k) > jump:
                jump = len(k)
            moves[len(k)] = moves.get(len(k), []) + [k]

        if jump == 2:  # if we are hoping over once then it must be a beating hop
            beating_hop = list(
                filter(lambda k: Checker.L1_norm(k[0], k[1]) == 4, moves[2]))
            if len(beating_hop) > 0:
                moves[2] = beating_hop

        # randomly chossing one hop from the collection of all deepest hops
        move = random.choice(moves[jump])
        return move[::-1]

    def start(self) -> None:
        """starts the game"""
        side = 'w'  # first move is of white
        count = 0  # number of moves are zero
        charge = True  # parity is True right now
        while self.count['b'] > 0 and self.count['w'] > 0 and charge:
            # printing the board and count
            self.print_board()
            print('\nBlack: ', self.count['b'])
            print('White: ', self.count['w'])
            print('Move:', count, end='\n\n')

            if side == 'w':
                # human playing from the side
                if self.human:
                    path = self.human_move()
                else:
                    path = self.computer_move('w')
            else:
                # computer playing from the side
                path = self.computer_move('b')
            self.move(path, side)
            # channging the side for next move
            side = 'b' if side == 'w' else 'w'
            count += 1
            # checking the parity
            charge = (self.parity['w'][0]
                      and self.parity['b'][0]) or (self.parity['w'][1]
                                                   and self.parity['b'][1])

        if not charge:  # if game draws
            print('Game draws :( in ', end='')
        elif self.count['b'] == 0:  # if white wins
            print('White wins! in ', end='')
        else:  # if black wins
            print('Black wins! in ', end='')
        print(count, 'moves.')


game = Checker(False, True)
game.start()
