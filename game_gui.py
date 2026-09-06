""" GUI for 'The Count """
from collections import deque
from os import makedirs

from os.path import join
from os.path import abspath
from os.path import isfile

from tkinter import Tk

from imgdict.get_dict_img import get_ico
from rooms.exchange import Exchange

from widgets.entry_container import EntryContainer
from widgets.sihir_scrolled_text import SihirScrolledText

from utils.string_builder import StringBuilder
from utils.command_router import CommandRouter

from game_machine import StateMachine


class Gui:
    """ ... """

    def __init__(self,
                 master: Tk,
                 machine: StateMachine) -> None:
        """ ... """

        self.master = master
        self._in_queue = deque()
        self._machine = machine
        self.limit_lines = 1000

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

        # self.txt.bind(
        #     "<Button-1>",
        #     lambda event: master.after_idle(self.entry.focus_set)
        # )

        self.bld = StringBuilder()
        self.entry.control.focus_set()

        router = CommandRouter()
        router.subscribe('auto', self.auto)

        master.after(100, self._update)

        self.process_input()

    def _update(self):
        """ ... """

        output = Exchange.output
        while output:
            text = output.popleft()
            self.print(text)

        self.master.after(100, self._update)

    def _command(self, key: str, command: str) -> None:
        """ ... """

        self.entry.clear()
        self._in_queue.append(command)

    def print(self, message: str):
        """ ... """

        bld = self.bld
        if message == '[CLEAR]':
            bld.clear()
        else:
            bld.append_line(message)
            count = bld.count_lines()
            if count > self.limit_lines:
                pos = bld.position(number = count - self.limit_lines)
                bld.delete(0, pos)

        self.txt.text = str(bld)

    def process_input(self):
        """ ... """

        if self._in_queue:
            command = self._in_queue.popleft()
            self._machine.do_command(command)

        self.master.after(200, self.process_input)

    def auto(self, noun: str):
        """ ... """

        output = Exchange.output
        full = join(abspath("."), "auto")
        output.append(full)
        makedirs(full, exist_ok=True)
        file = join(full, f'script_{noun}.txt')
        if not isfile(file):
            output.append(f"I can't find {file}")
            return False

        with open(file=file, mode='rt', encoding='utf-8') as stream:
            for line in stream:
                if line.startswith('#'):
                    continue
                self._in_queue.append(line.strip())
