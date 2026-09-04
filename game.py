""" GUI for 'The Count """

from tkinter import Tk

from collections import deque

from handlers import game

from imgdict.get_dict_img import get_ico
from rooms.bedroom import Bedroom

from widgets.entry_container import EntryContainer
from widgets.sihir_scrolled_text import SihirScrolledText

from utils.string_builder import StringBuilder
from utils.command_router import CommandRouter

from state import StateMachine

from handlers import GameState


class Gui:
    """ ... """

    def __init__(self, master: Tk) -> None:
        """ ... """

        self.master = master

        icon = get_ico(key='vampire.ico', size=(22, 22))
        master.iconphoto(False, icon, icon)  # noqa

        master.title("The Count, Scott Adams 1979")
        master.grid_rowconfigure(0, weight=1)
        master.grid_rowconfigure(1, weight=0)

        master.grid_columnconfigure(0, weight=1)

        self.txt = SihirScrolledText(master)
        self.txt.grid(
            row=0,
            column=0,
            padx=1,
            pady=1,
            sticky="news")

        self.entry = EntryContainer(
            master=master,
            key='command',
            prompt='Command',
            prompt_width=10,
            on_return=self._command)

        self.entry.grid(
            row=1,
            column=0,
            padx=10,
            pady=4,
            sticky="news")

        self.bld = StringBuilder()
        self.entry.control.focus_set()

        master.after(100, self._update)

        game.start()

    def _update(self):
        """ ... """

        output = GameState.output()
        while output:
            text = output.popleft()
            self.print(text)

        self.master.after(100, self._update)

    def _command(self, key: str, command: str) -> None:
        """ ... """

        self.print("* " + command)
        self.entry.clear()
        StateMachine.do_command(command)

    def print(self, message: str):
        """ ... """

        bld = self.bld
        if message == '[CLEAR]':
            bld.clear()
        else:
            bld.append_line(message)
            count = bld.count_lines()
            if count > 100:
                pos = bld.position(number = count - 100)
                bld.delete(0, pos)

        self.txt.text = str(bld)
