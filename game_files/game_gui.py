""" GUI for 'The Count """

from collections import deque
from os import makedirs

from os.path import join
from os.path import abspath
from os.path import isfile

from sys import argv

from tkinter import Tk, messagebox
from tkinter import simpledialog

from imgdict.get_dict_img import get_ico
from rooms.exchange import Exchange

from widgets.entry_container import EntryContainer
from widgets.sihir_scrolled_text import SihirScrolledText

from utils.string_builder import StringBuilder
from utils.command_router import CommandRouter

from game_files.game_machine import StateMachine

from data import delay


class Gui:
    """ ... """

    def __init__(self,
                 master: Tk,
                 machine: StateMachine) -> None:
        """ ... """

        self.blink = 200
        iarg = iter(argv[1:])
        for arg in iarg:
            if arg == "--delay":
                self.blink = int(next(iarg))

        self.master = master
        self._in_queue = deque()
        self._machine = machine
        self.limit_lines = 1000
        self.after_ident = None

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

        self.txt.bind("<Button-1>", self.text_click)

        self.bld = StringBuilder()
        self.entry.control.focus_set()

        router = CommandRouter()
        router.subscribe('auto', self.auto)
        router.subscribe('moves', self.get_moves)

        master.after(100, self._update)

        self.process_input()

    def text_click(self, event) -> None:
        """ ... """

        if self.after_ident is None:
            self.after_ident = event.widget.after(200, self.set_entry_focus)
        else:
            event.widget.after_cancel(self.after_ident)
            self.after_ident = None

    def set_entry_focus(self):
        """ ... """

        self.after_idnt = None
        self.entry.control.focus_set()

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

        result = True
        if self._in_queue:
            command = self._in_queue.popleft()
            result = self._machine.do_command(command)
            if not result:
                ...
                self.print(str(result))

        if self._in_queue and not result:
            if not messagebox.askyesno('Command Failed',
                                       'Continue processing?'):
                self._in_queue.clear()

        self.master.after(self.blink, self.process_input)

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
                line = line.strip()

                if line.upper() == 'HALT':
                    return

                self._in_queue.append(line)

    def get_moves(self) -> tuple[int, int] | None:
        """ ... """

        answer = simpledialog.askstring(title='Moves',
                                        prompt='Enter day,move',
                                        initialvalue='1,1')
        if answer:
            values = answer.split(',')
            if (len(values) == 2):
                return (int(values[0]), int(values[1]))

        return None