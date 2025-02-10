import os
from Grid import Grid


def run():
    """
    This function is meant to run the backtracking algorithm
    :return: None
    """
    ########################################################
    # Console Configuration
    ########################################################
    # Set Encoder to UTF-8
    os.system('chcp 65001')

    # Set window size
    #os.system('mode con: cols=40 lines=18')
    # Set window name
    os.system("title Sudoku - Backtracking Solution")

    # Clear Console
    clear = lambda: os.system('cls')
    clear()

    ########################################################
    # Solve The Sudoku
    ########################################################
    # Start solving the board
    grid = Grid(0.01)
    grid.backtracking()

    ########################################################
    # End of Program
    ########################################################
    # Grid is solved
    input("\nThe Grid is solved! (press Enter to exit)")
    return
