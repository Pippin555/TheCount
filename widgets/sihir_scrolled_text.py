""" file list implementation """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2024-2024 all rights reserved"

from typing import Callable
from typing import Optional

from tkinter.scrolledtext import ScrolledText
from tkinter import INSERT
from tkinter import END


# pylint: disable=too-many-ancestors
class SihirScrolledText(ScrolledText):
    """ a text box that can scroll """

    def __init__(self, *args, **kwargs):

        self._move_event: Optional[Callable]  = None
        if 'move_event' in kwargs:
            self._move_event = kwargs.pop('move_event')

        super().__init__(*args, **kwargs)

        self._modified = False

        # Bind custom key events
        self.bind("<KeyPress>", self.on_key_press, add='+')
        self.bind('<KeyRelease>', self._update_line_number, add='+')

        # Bind events for left and right mouse clicks
        self.bind('<ButtonRelease-1>', self._update_line_number, add='+')
        self.bind('<ButtonRelease-3>', self._update_line_number, add='+')
        self.bind("<<Modified>>", self._on_text_changed)

    def on_key_press(self, event):
        """ key press event handler """

        # print(f 'event state 0x{event.state:5x}')
        if event.keysym == "Return":
            return self._handle_enter_key(event)

        # Check if Control is pressed
        if event.keysym == "Delete" and (event.state & 0x0004 != 0x0):
            # print(f 'handle control delete 0x{event.state:5x}')
            return self._handle_control_delete()

        # check if Shift is pressed
        if event.keysym == "Delete" and (event.state & 0x0001 != 0x0):
            # print(f 'handle shift delete 0x{event.state:5x}')
            return self._handle_shift_delete()

        return None

    def _handle_control_delete(self):
        """ remove current line """

        # Get the start of the current line and the end of the next line
        row, col = self.cursor_pos()

        start_of_current_line = f"{row}.0"

        # then find out where the beginning of the next line is
        start_of_next_line = f"{row + 1}.0"

        # remove everything in between
        self.delete(start_of_current_line, start_of_next_line)

        # now try to move the cursor back to the cursor position at the
        # beginning, but now in the current line, if the line is long enough

        end_of_current_line = f'{row}.end'
        text = self.get(start_of_current_line, end_of_current_line)

        # col may be no higher than the line length
        # this causes the cursor to move back along shorter lines
        # but that is cosmetic for the simple widget
        col = min(col, len(text))
        new_cursor_position = f'{row}.{col}'
        self.mark_set(INSERT, new_cursor_position)
        return 'break'

    def _handle_shift_delete(self):
        # Get the current position of the cursor

        cursor_position = self.index("insert")
        end_of_line = f"{cursor_position.split('.', maxsplit=1)[0]}.end"

        # Remove everything from the cursor position to the end of the line
        self.delete(cursor_position, end_of_line)

    def _update_line_number(self, event):
        """ Get the current cursor position """

        _ = event  # not used, always provided

        # you can use a subscription on this event
        # to show the cursor position on the GUI
        if self._move_event:
            row, col = self.cursor_pos()
            self._move_event(row=row, col=col)

    def cursor_pos(self):
        """  current cursor position """

        cursor_position = self.index(INSERT)
        return map(int, cursor_position.split('.'))

    @property
    def current_line(self) -> str:
        """ return the whole line
        @return: str
        """

        row, _ = self.cursor_pos()
        start_of_current_line = f"{row}.0"
        end_of_current_line = f'{row}.end'
        return self.get(start_of_current_line, end_of_current_line)

    @staticmethod
    def _leading_spaces(line: str):
        """ iterate over the spaces at the beginning of the line
        @return: str
        """

        result = ''
        for c in iter(line):
            if not c.isspace():
                break
            result += c

        return result

    def _handle_enter_key(self, event):
        """ match the leading spaces
        @param event:
        @return: 'break'
        """

        _ =  event  # not used but always provided

        leading = SihirScrolledText._leading_spaces(self.current_line)

        # Insert line feed and spaces at the current cursor position
        self.insert(INSERT, '\n' + leading)
        return 'break'

    def _on_text_changed(self, event):
        """ script_area changed """

        _ = event

        # Check if the text widget is modified
        if self.edit_modified():
            self._modified = True
            # Reset the modified flag
            self.edit_modified(False)

    @property
    def modified(self):
        """ get the modified flag """

        return self._modified

    @modified.setter
    def modified(self, value: bool):
        """ set the modified flag """

        self._modified = value

    @property
    def text(self) -> str:
        """ get the contained text """

        return self.get("1.0", END)

    @text.setter
    def text(self, value: str):
        """ set the text """

        self.delete("1.0", END)
        self.insert(END, value)
        self._modified = False
