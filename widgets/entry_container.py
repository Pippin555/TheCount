""" the container for an entry with prompt and unit labels """

__author__ = 'Sihir'
__copyright__ = '© Sihir 2023-2025 all rights reserved'

from typing import Callable

from tkinter import Button
from tkinter import Label
from tkinter import Misc
from tkinter import Frame
from tkinter import Entry
from tkinter import StringVar
from tkinter import Widget

from imgdict.get_dict_img import get_ico


class EntryContainer(Frame):
    """ entry and its StringVar """

    def __init__(self,
                 master: Misc,
                 **kwargs):
        """ initialize the Label, Entry and StringVar """

        super().__init__(master=master)

        self.grid_columnconfigure(index=0, weight=0)
        self.grid_columnconfigure(index=1, weight=1)

        self._key = kwargs.get('key', '')
        padx = kwargs.get('padx', 2)  # noqa
        pady = 0  # noqa
        back_color = kwargs.get('bg', 'lightgrey')  # noqa
        entry_bg = kwargs.get('entry_background', 'white')
        prompt = kwargs.get('prompt', '')
        prompt_width = kwargs.get('prompt_width', len(prompt) + 5)
        use_clear = kwargs.get('clear', True)

        self._key = kwargs.get('key', '')
        if self._key == '':  # compatibility
            self._key = kwargs.get('tag', '')

        self._on_return: Callable| None = kwargs.get('on_return', None)

        show = kwargs.get('show', '')

        command: Callable | None = kwargs.get('command', None)

        if command is not None:
            prompt_control = Button(
                master=self,
                width=prompt_width,
                text=prompt,
                background=back_color,
                anchor='w',
                command=command
            )

        else:
            prompt_control = Label(
                master=self,
                width=prompt_width,
                text=prompt,
                background=back_color,
                anchor='w',
                justify='left')

        self.prompt_control = prompt_control

        column = 0
        if prompt_width > 0:
            self.grid_columnconfigure(column, weight=0)  # label

            prompt_control.grid(
                row=0,
                column=column,
                padx=padx,
                pady=0,
                sticky='wns')

            column += 1

        str_value = StringVar(master=self,
                              value=kwargs.get('value', ''))

        self.tag = kwargs.get('tag', None)
        if self.tag is None:
            self.tag = prompt

        entry_width = kwargs.get('width', 10)
        entry = Entry(master=self,
                      width=entry_width,
                      background=entry_bg,
                      textvariable=str_value,
                      show=show)

        # frame.configure(height=entry.winfo_reqheight())

        self.grid_columnconfigure(index=column, weight=1)  # label

        entry.grid(row=0,
                   column=column,
                   padx=padx,
                   pady=pady,
                   sticky='news')

        self.entry = entry
        column += 1

        unit_width = kwargs.get('unit_width', 0)
        unit_text = kwargs.get('unit_text', '')

        self.label_unit = Label(master=self,
                                width=unit_width,
                                background=back_color,
                                text=unit_text)

        self.setup = {'frame': self,
                      'prompt': prompt_control,
                      'value': str_value,
                      'entry': entry,
                      'entry_width': entry_width}

        if unit_width > 0:
            self.grid_columnconfigure(column, weight=0)  # unit
            self.label_unit.grid(row=0,
                                 column=column,
                                 padx=padx,
                                 pady=pady,
                                 sticky='news')
            column += 1
            self.setup['unit'] = self.label_unit

        if use_clear:
            clear_ico = get_ico('clear.ico', (16, 16))

            clear_button = Button(master=self,
                                  image=clear_ico,  # type: ignore
                                  command=self.clear)

            clear_button.grid(row=0,
                              column=column,
                              padx=(4, 0),
                              pady=0,
                              sticky='news')

            self.setup['clear_button'] = clear_button

        if self._on_return is not None:
            entry.bind('<Return>', self._on_my_return)

        self.after_idle(self._check_row_heights)  # noqa

    def _on_my_return(self, event):
        """ ... """

        _ = event
        self._on_return(self._key, self.value)

    def _check_row_heights(self):
        """ ... """

        # print(f'{self.winfo_height()}')
        # row = int(self.grid_info()['row'])
        # for child in self.master.grid_slaves(row=row):
        #     print(child, child.winfo_reqheight())

    def focus(self):
        """ set the focus to the entry """

        self.entry.focus_set()

    @property
    def prompt(self) -> Widget :
        """ ... """

        return self.prompt_control

    @property
    def control(self) -> Entry:
        """ return the frame """

        return self.entry

    def get_value(self):
        """ ... """

        str_value = self.setup['value']
        return str_value.get()

    @property
    def value(self) -> str:
        """ return the value """

        str_value = self.setup['value']
        return str_value.get()

    @value.setter
    def value(self, data: str):
        """ set the value """

        str_value = self.setup['value']
        str_value.set(data)
        self.entry.select_range(0, 'end')

    def clear(self):
        """ clear the entry value """

        self.value = ''

    @property
    def unit(self):
        """ the unit of the value """

        return self.label_unit.cget('text')

    @unit.setter
    def unit(self, value: str):
        """ set the unit """

        self.label_unit.config(text=value)

    @property
    def width(self):
        """ get the entry width """
        return self.setup['entry_width']

    @width.setter
    def width(self, value: int):
        """ set and save the entry width """

        self.setup['entry_width'] = value
        self.setup['entry'].config(width=value)

    @property
    def my_tag(self):
        """ get the tag """

        return self._key

    @property
    def key(self):
        """ get the key """

        return self._key

    @property
    def show(self):
        """ ... """

        return self.entry.cget('show')

    @show.setter
    def show(self, value: bool):
        """ ... """

        self.entry.config(show='' if value else '*')
