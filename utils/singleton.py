""" Singleton metaclass """

__author__ = 'Sihir'
__copyright__ = '© Sihir 2021-2025 all rights reserved'


class Singleton(type):
    """
    A metaclass that ensures a class has only one instance.

    Classes using this metaclass will return the same instance every time
    they are instantiated. This is useful for globally shared components
    like configuration managers, routers, or state coordinators.

    Example:
        class MySingleton(metaclass=Singleton):
            pass

        a = MySingleton()
        b = MySingleton()
        assert a is b  # True

    Internal:
        Instances are stored in a private class-level dictionary `_instances`.

    Note:
        to remove the instance of class MySingeleton use:

        MySingleton.reset_instance()

    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """ this is run when an instance is created """

        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]

    def reset_instance(self):
        """
        remove the instance of class cls

        usage: MySingleton.reset_instance()
        """

        self._instances.pop(self, None)
