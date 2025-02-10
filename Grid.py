import os
import time
from Color import Color


class Grid:
    def __init__(self, throttle=0.1):
        # Initiate utilities
        self.color = Color()
        # Initiate Algorithm Variables
        self.step_cnt = 0
        self.is_advancing = True
        # Initiate Current Cell Variables
        self.x = 0
        self.y = 0
        # Initiate Boards
        self.CONST_BOARD = self.getBoard()
        self.board = self.getBoard()
        # System Control Variables
        self.throttle = throttle

    @staticmethod
    def getBoard():
        """
        This function reads and saves a Sudoku grid
        :return: (int[][]) The sudoku grid
        """
        ########################################################
        # Initialization
        ########################################################
        # Initialize the sudoku grid
        board = [[], [], [], [], [], [], [], [], []]

        # Initialize a counter
        i = 0

        ########################################################
        # Get Data From File
        ########################################################
        # Open Text file
        f = open("Grid.txt", "r")
        # Go through the lines of the file
        for line in f.readlines():
            # Iterate through the characters
            for char in line:
                # Verify the character
                if char != "\n":
                    board[i].append(int(char))

            # Increment counter
            i += 1

        ########################################################
        # End of Function
        ########################################################
        return board

    def backtracking(self):
        """
        This is a recursive backtracking function that solves a sudoku grid
        :return: None
        """
        # Declare a throttle
        time.sleep(self.throttle)

        ########################################################
        # Current Cell Is A Constant
        ########################################################
        # Check if current cell is a constant
        if self.CONST_BOARD[self.y][self.x] != 0:

            # Check if Sudoku is going forward
            if self.is_advancing:

                # Last cell of the grid has been reached
                if [self.x, self.y] == [8, 8]:
                    # Verify that it is filled completely
                    if not self.isSolved():
                        # Display error
                        print("Error! Last cell has been reached but grid is not filled completely")

                    # We exit the recursive
                    self.is_advancing = False

                # End of Row has been reached
                elif self.x == 8:
                    # Jump to next row
                    self.x = 0
                    self.y += 1
                    self.backtracking()

                # Keep traveling in the row
                else:
                    # Jump to next cell
                    self.x += 1
                    self.backtracking()

        ########################################################
        # Current Cell Is Not A Constant
        ########################################################
        else:
            for number in range(1, 10):

                # Verify if value breaks the board
                if self.isValid(number):
                    # Insert Value
                    self.board[self.y][self.x] = number
                    # Display Grid
                    self.displayBoard()
                    # Declare intention to move forward
                    self.is_advancing = True

                    # Last cell has been reached
                    if [self.x, self.y] == [8, 8]:
                        # Verify if it is not filled completely
                        if not self.isSolved():
                            print("Error! Last cell has been reached but grid is not filled completely")

                        # We exit the recursive
                        self.is_advancing = False
                        break

                    # End of the row has been reached
                    elif self.x == 8:
                        # Go to next cell
                        self.x = 0
                        self.y += 1
                        self.backtracking()

                    # Keep going forward
                    else:
                        # Go to next cell
                        self.x += 1
                        self.backtracking()

                    # Verify if the Grid has been solved
                    if self.isSolved():
                        break

                # All values for this cell breaks the board
                if number == 9 and not self.isValid(number):
                    # Reset value of the cell
                    self.board[self.y][self.x] = 0
                    # Back track to previous cell
                    self.is_advancing = False
                    break

        ########################################################
        # Return to Previous Cell
        ########################################################
        # Check if end of row
        if self.x == 0:
            # Jump to next row
            self.x = 8
            self.y -= 1
        # End of row not reached
        else:
            # Jump to next cell in row
            self.x -= 1
        # Go to previous cell
        return

    def displayBoard(self):
        """
        This function displays the current state of the sudoku grid
        :return: None
        """
        ########################################################
        # Initialization
        ########################################################
        # Formatting Symbols
        empty_cell = "•"  # #empty_cell = 0 #empty_cell = "·"
        hor_sep = "-------------------------------"
        vert_sep = "|"

        # Declare the display string
        display = ""

        ########################################################
        # Construct The Display
        ########################################################
        # Iterate through the rows
        for y in range(0, 9):
            # Add Horizontal seperator per Region
            if y in [0, 3, 6]:
                display += (hor_sep + "\n")

            # Iterate through the columns
            for x in range(0, 9):
                # Add vertical seperator for this row
                if x in [0, 3, 6]:
                    display += vert_sep

                # Cell Not Filled Yet
                if self.board[y][x] == 0:
                    display += f"{self.color.RED} {empty_cell} {self.color.RESET}"
                # Cell Filled
                elif self.board[y][x] != self.CONST_BOARD[y][x]:
                    display += f"{self.color.GREEN} {self.board[y][x]} {self.color.RESET}"
                # Cell is constant
                else:
                    display += f"{self.color.WHITE} {self.board[y][x]} {self.color.RESET}"

                # Add last vertical seperator for this row
                if x == 8:
                    display += vert_sep

            # Jump to next row
            display += "\n"

            # Add Last horizontal seperator
            if y == 8:
                display += (hor_sep + "\n")

        # Increment the global counter
        self.step_cnt += 1
        # Add a Step display
        display += f"Steps: {self.step_cnt}"

        ########################################################
        # Display the Grid
        ########################################################
        # Clear Console
        clear = lambda: os.system('cls')
        clear()

        # Display new Grid
        print(display)

    def isValid(self, number):
        """
        This function verifies if a certain value can be placed in a sudoku.
        :return: (bool) True if teh value does not break the board
        """
        ########################################################
        # Check the row
        ########################################################
        row = []
        # Save row values
        for value in self.board[self.y]:
            row.append(value)

        # Exit if value already present
        if number in row:
            return False

        ########################################################
        # Check the column
        ########################################################
        column = []
        # Save column values
        for r in range(0, 9):
            column.append(self.board[r][self.x])

        # Exit if value already present
        if number in column:
            return False

        ########################################################
        # Check the sub-grid
        ########################################################
        # Get region coordinates
        region_x = self.x // 3
        region_y = self.y // 3

        region = []
        # Save sub-grid values
        for px in range(region_x * 3, (region_x + 1) * 3):
            for py in range(region_y * 3, (region_y + 1) * 3):
                region.append(self.board[py][px])

        # Exit if present
        if number in region:
            return False

        ########################################################
        # All Checks Passed Successfully
        ########################################################
        return True

    def isSolved(self):
        """
        This function verifies if the sudoku has been completely filled
        :return: True if the board is completely filled
        """
        # Initiate the value to True
        solved = True

        # Verify if there is some empty cells left
        for row in range(0, 9):
            if 0 in self.board[row]:
                # Change value to False if empty cell
                solved = False

        # End
        return solved
