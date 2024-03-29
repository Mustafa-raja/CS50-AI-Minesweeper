import itertools
import random
import copy
from termcolor import colored

class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=12):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def get_set(self):
        return self.cells

    def get_set_length(self):
        return len(self.cells)

    def get_count(self):
        return self.count

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        cell = copy.deepcopy(self.cells)
        if len(cell) == self.count:
            return cell
        else:
            return None

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        cell = copy.deepcopy(self.cells)
        if self.count == 0:
            return cell
        else:
            return None

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):

        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=9, width=9):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        # print("heheheheheehhehehe")
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # print(self.moves_made)
        mangoes = set()
        # print(cell)
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i, j) == cell or self.moves_made.__contains__((i, j)) or self.safes.__contains__((i, j)):
                    continue
                if 0 <= i < self.height and 0 <= j < self.width:
                    # print(f"({i}, {j})")
                    mangoes.add((i, j))

        # for mango in mangoes:
        #     print(mango)
        self.moves_made.add(cell)
        self.mark_safe(cell)

        self.knowledge.append(Sentence(mangoes, count))

        # print("knowledge")
        for e in self.knowledge:
            if e.get_count() == 0:
                size = e.get_set_length()
                for cell in range(size):
                    (i,j) = e.get_set().pop()
                    print(colored(f"marking cell {(i,j)} as safe move",  'green'))
                    self.mark_safe((i,j))
            elif e.get_count() == e.get_set_length():
                size = e.get_set_length()
                for cell in range(size):
                    the_cell = e.get_set().pop()
                    print(colored(f"marking cell {the_cell} as mine", 'red'))
                    self.mark_mine(the_cell)
                    # for i in range(the_cell[0] - 1, the_cell[0] + 2):
                    #     for j in range(the_cell[1] - 1, the_cell[1] + 2):
                    #         if (i, j) == the_cell or self.mines.__contains__((i, j)) or self.moves_made.__contains__(
                    #                 (i, j)):
                    #             print("moving forward")
                    #             continue
                    #         if 0 <= i < self.height and 0 <= j < self.width:
                    #             print(e.get_set())

        for sentence in self.knowledge:
            if sentence.get_set_length() == 0:
                continue
            count = 0

            for cell in sentence.get_set():
                if self.mines.__contains__(cell):
                    count += 1
            if sentence.count == count:
                size = sentence.get_set_length()
                for i in range(size):
                    cell = sentence.get_set().pop()
                    if self.mines.__contains__(cell) or self.moves_made.__contains__(cell):
                        continue
                    else:
                        (i,j) = cell
                        print(f"marking cell {(i,j)} as safe move")
                        self.mark_safe(cell)
            print(sentence)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for move in self.safes:
            if move in self.moves_made:
                (i,j) = move
                # print(f"safe move {(i,j)} has already been made")
            else:
                return move
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        for i in range(self.width - 1):
            for j in range(self.height - 1):

                if (i, j) in self.mines or (i, j) in self.moves_made:
                    print(f"move {(i, j)} has already been made or is booked by AI as a known mine")
                else:
                    print(f"move {(i, j)} made")
                    return (i, j)
