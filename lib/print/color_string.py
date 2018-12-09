from colorama import Fore, Style, init
from enum import Enum, auto

init()


class Color(Enum):
    grey = auto()
    white = auto()
    red = auto()
    blue = auto()
    yellow = auto()
    green = auto()
    magenta = auto()
    cyan = auto()
    default = auto()


class ColorString():
    def __init__(self, raw_string='', color=Color.default):
        if not isinstance(raw_string, str):
            raise TypeError
        self._raw = raw_string
        self._colored = self.__get_colored_string(self._raw, color)

    def __get_colored_string(self, raw_string, color):
        colored_string = raw_string
        if color == Color.default:
            colored_string = Fore.RESET + colored_string
        elif color == Color.grey:
            colored_string = Fore.LIGHTBLACK_EX + colored_string
        elif color == Color.white:
            colored_string = Fore.WHITE + colored_string
        elif color == Color.red:
            colored_string = Fore.LIGHTRED_EX + colored_string
        elif color == Color.blue:
            colored_string = Fore.LIGHTBLUE_EX + colored_string
        elif color == Color.yellow:
            colored_string = Fore.LIGHTYELLOW_EX + colored_string
        elif color == Color.green:
            colored_string = Fore.LIGHTGREEN_EX + colored_string
        elif color == Color.magenta:
            colored_string = Fore.LIGHTMAGENTA_EX + colored_string
        elif color == Color.cyan:
            colored_string = Fore.LIGHTCYAN_EX + colored_string

        colored_string = colored_string + Style.RESET_ALL

        return colored_string

    def __str__(self):
        return self._colored

    def __len__(self):
        return len(self._raw)

    def __add__(self, other):
        new_color_string = ColorString()

        if isinstance(other, self.__class__):
            new_color_string._raw = self._raw + other._raw
            new_color_string._colored = self._colored + other._colored
        elif isinstance(other, str):
            new_color_string._raw = self._raw + other
            new_color_string._colored = self._colored + other
        else:
            raise TypeError

        return new_color_string

    def __radd__(self, other):
        new_color_string = ColorString()

        if isinstance(other, self.__class__):
            new_color_string._raw = other._raw + self._raw
            new_color_string._colored = other._colored + self._colored
        elif isinstance(other, str):
            new_color_string._raw = other + self._raw
            new_color_string._colored = other + self._colored
        else:
            raise TypeError

        return new_color_string

    def __mul__(self, integer):
        new_color_string = ColorString()
        new_color_string._raw = self._raw * integer
        new_color_string._colored = self._colored * integer
        return new_color_string

    __rmul__ = __mul__
