""" main program of The Count together with ChatGPT a revival of the old RPG game """

from sys import exit as _exit

from tkinter import Tk

from game_files.game_gui import Gui
from game_files.game_state import GameState
from game_files.game_handlers import GameHandler
from game_files.game_machine import StateMachine


def main() -> int:
    """ """

    game_state = GameState()
    game_handler = GameHandler(game=game_state)
    game_machine = StateMachine(game=game_state,
                                handler=game_handler)

    root = Tk()
    root.protocol("WM_DELETE_WINDOW", root.destroy)
    gui = Gui(root,
              machine=game_machine)

    root.mainloop()
    del gui
    return 0

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    _exit(main())

