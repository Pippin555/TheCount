""" GUI for 'The Count """

from tkinter import Tk

from handlers import game
from handlers import GameState
from imgdict.get_dict_img import get_ico

from widgets.entry_container import EntryContainer
from widgets.sihir_scrolled_text import SihirScrolledText

from utils.string_builder import StringBuilder
from utils.command_router import CommandRouter

from state import StateMachine


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

        CommandRouter().subscribe('log', self.output)

        game.start()

    def _command(self, key: str, command: str) -> None:
        """ ... """

        self.output("* " + command)
        self.entry.clear()
        response = StateMachine.do_command(command)
        self.output(response)

    def output(self, message: str):
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
