""" main program of The Count together with ChatGPT a revival of the old RPG game """

from sys import exit as _exit

from tkinter import Tk

from game import Gui


def main() -> int:
    """ """

    root = Tk()
    root.protocol("WM_DELETE_WINDOW", root.destroy)
    gui = Gui(root)
    root.mainloop()
    del gui
    return 0

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    _exit(main())

