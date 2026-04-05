from colorama import init, Fore
import tqdm

init()

def Reset():
    print(Fore.RESET, end="")

def _PrinterGenerator(color):
    def Printer(*args, sep=" "):
        string = sep.join([str(item) for item in args])
        return getattr(Fore, color)+string+Fore.RESET
    return Printer

def _StarterGenerator(color):
    def Starter():
        print(getattr(Fore, color), end="")
    return Starter

class ColoredTqdm(tqdm.tqdm):
    def __init__(self, iterable=None, desc=None, total=None, leave=True, file=None,
                 ncols=None, mininterval=0.1, maxinterval=10.0, miniters=None,
                 ascii=None, disable=False, unit='it', unit_scale=False,
                 dynamic_ncols=False, smoothing=0.3, bar_format=None, initial=0,
                 position=None, postfix=None, unit_divisor=1000, write_bytes=False,
                 lock_args=None, nrows=None, colour=None, delay=0.0, gui=False,
                 **kwargs):
        super().__init__(iterable, desc, total, leave, file,
                 ncols, mininterval, maxinterval, miniters,
                 ascii, disable, unit, unit_scale,
                 dynamic_ncols, smoothing, bar_format, initial,
                 position, postfix, unit_divisor, write_bytes,
                 lock_args, nrows, colour or "#1fd18b", delay, gui,
                 **kwargs)
    
    def close(self):
        super().close()

def _makeAll():
    colors = [
        "Black",
        "Red",
        "Green",
        "Yellow",
        "Blue",
        "Magenta",
        "Cyan",
        "White",
        "LightBlack_EX",
        "LightRed_EX",
        "LightGreen_EX",
        "LightYellow_EX",
        "LightBlue_EX",
        "LightMagenta_EX",
        "LightCyan_EX",
        "LightWhite_EX",
    ]
    for color in colors:
        globals()[f"Fore{color.replace('_EX', '')}"] =  _PrinterGenerator(color.upper())
        globals()[f"Start{color.replace('_EX', '')}"] =  _StarterGenerator(color.upper())

_makeAll()

__all__ = [
    "Reset",
    "ColoredTqdm",
    "ForeBlack",
    "ForeRed",
    "ForeGreen",
    "ForeYellow",
    "ForeBlue",
    "ForeMagenta",
    "ForeCyan",
    "ForeWhite",
    "ForeLightBlack",
    "ForeLightRed",
    "ForeLightGreen",
    "ForeLightYellow",
    "ForeLightBlue",
    "ForeLightMagenta",
    "ForeLightCyan",
    "ForeLightWhite",
    "StartBlack",
    "StartRed",
    "StartGreen",
    "StartYellow",
    "StartBlue",
    "StartMagenta",
    "StartCyan",
    "StartWhite",
    "StartLightBlack",
    "StartLightRed",
    "StartLightGreen",
    "StartLightYellow",
    "StartLightBlue",
    "StartLightMagenta",
    "StartLightCyan",
    "StartLightWhite",
]
