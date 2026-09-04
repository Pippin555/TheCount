""" commands can be sent and received by anyone """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2025-2025 all rights reserved"
__origin__ = 'ChatGPT'

import weakref

from enum import Enum
from enum import auto

from typing import List
from typing import Dict
from typing import Any
from typing import Callable

from utils.singleton import Singleton


class HandleResult(Enum):
    COMMAND_IGNORED = auto()


class CommandRouter(metaclass=Singleton):
    """ A global command distribution hub.

        The CommandRouter allows any part of the program to
        send and receive commands without direct references.
        Components can subscribe to specific commands using
        `subscribe(command, handler)` and invoke commands
        with `handle(command, *args, **kwargs)`, this is a
        one-to-one communication.

        When the function 'broadcast(*args,**kwargs)' is used
        the communication becomes one-to-many and all answers
        are collected and sent back to the caller.

        This enables loose coupling between UI elements,
        database handlers, players, and dialogs, allowing the
        system to grow modularly and respond dynamically to
        user interaction.

        Example:
        CommandRouter().subscribe("play_song", self.play_selected_song)
        result = CommandRouter().handle("play_song", filename)
        results:[] = CommandRouter().broadcast('refresh')

        Commands are dispatched to all subscribers in the order they were registered.
    """

    def __init__(self):
        """ initialize the class """

        self.clear()

    def clear(self):
        """ ... """

        self.subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, command: str, handler: Callable) -> None:
        """ Register a handler for a specific command. """

        subscribers = self.subscribers.setdefault(command, [])

        for subscriber in subscribers:
            existing = subscriber() if isinstance(subscriber, weakref.WeakMethod) else subscriber
            if existing == handler:
                raise ValueError(
                    f"Handler {handler!r} already subscribed for {command!r}"
                )

        # Wrap bound methods in weakref, keep functions as-is
        if hasattr(handler, "__self__") and handler.__self__ is not None:  # noqa
            subscribers.append(weakref.WeakMethod(handler))
        else:
            subscribers.append(handler)

    def unsubscribe(self, command: str, handler: Callable) -> None:
        """ Remove a handler subscription. """

        handlers = self.subscribers.get(command, [])
        for h in handlers[:]:
            if isinstance(h, weakref.WeakMethod):
                if h() == handler:
                    handlers.remove(h)
                    break
            else:
                if h == handler:
                    handlers.remove(h)
                    break

        if not handlers:
            self.subscribers.pop(command, None)

    def handle(self, command: str, *args, **kwargs) -> Any:
        """ Send command to first interested subscriber. """

        handlers = self.subscribers.get(command, [])
        for h in handlers:
            func = h() if isinstance(h, weakref.WeakMethod) else h
            if func is None:
                # dead weakref - remove it
                handlers.remove(h)
                continue
            # one-to-one: call first alive handler
            return func(*args, **kwargs)

        return HandleResult.COMMAND_IGNORED

    def broadcast(self, command: str, *args, **kwargs) -> None:
        """ Send command to all interested subscribers, return None. """

        handlers = self.subscribers.get(command, [])

        dead_refs = []
        for h in handlers:
            func = h() if isinstance(h, weakref.WeakMethod) else h
            if func is None:
                dead_refs.append(h)
                continue
            func(*args, **kwargs)

        # Remove dead weakrefs safely  # noqa
        handlers[:] = [h for h in handlers if h not in dead_refs]

def command_handler(command: str):
    """Decorator to mark instance methods as handlers for a command.

    Usage:
        class MyClass:
            @command_handler("play")
            def play(self, ...):
                pass
    """
    def decorator(func):
        func._command_handler_for = command  # mark function for later registration
        return func
    return decorator


def register_handlers(obj):
    """Call this on instance to auto-subscribe all decorated methods."""

    router = CommandRouter()
    for attr_name in dir(obj):
        attr = getattr(obj, attr_name)
        if callable(attr) and hasattr(attr, "_command_handler_for"):
            router.subscribe(attr._command_handler_for, attr)  # noqa


class CommandNotHandledError(Exception):
    """Raised when a command is not handled by any subscriber."""

    def __init__(self, command):
        super().__init__(f"Command '{command}' was not handled by any subscriber.")
        self.command = command


def safe_handle(command, *args, **kwargs):
    """ try to execute the command router for the command """

    result = CommandRouter().handle(command, *args, **kwargs)
    if result == HandleResult.COMMAND_IGNORED:
        # the call failed
        raise CommandNotHandledError(command)

    return result
