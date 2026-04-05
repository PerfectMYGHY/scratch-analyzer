import tqdm
from typing import Iterable, Optional, Any

def Reset() -> None:
    ...

class ColoredTqdm(tqdm.tqdm):
    color2: str

    def __init__(self, iterable: Optional[Iterable] = ..., desc: Optional[str] = ...,
                 total: Optional[int] = ..., leave: bool = ..., file: Optional[Any] = ...,
                 ncols: Optional[int] = ..., mininterval: float = ...,
                 maxinterval: float = ..., miniters: Optional[Any] = ...,
                 ascii: Optional[Any] = ..., disable: bool = ..., unit: str = ...,
                 unit_scale: bool = ..., dynamic_ncols: bool = ...,
                 smoothing: float = ..., bar_format: Optional[Any] = ..., initial: int = ...,
                 position: Optional[Any] = ..., postfix: Optional[str] = ...,
                 unit_divisor: int = ..., write_bytes: Optional[Any] = ...,
                 lock_args: Optional[Any] = ..., nrows: Optional[int] = ...,
                 colour: Optional[str] = ..., delay: float = ..., gui: bool = ...,
                 **kwargs):
        ...
    
    def close(self):
        ...

def ForeBlack(*args, sep:str = ...) -> str:
    ...

def ForeRed(*args, sep:str = ...) -> str:
    ...

def ForeGreen(*args, sep:str = ...) -> str:
    ...

def ForeYellow(*args, sep:str = ...) -> str:
    ...

def ForeBlue(*args, sep:str = ...) -> str:
    ...

def ForeMagenta(*args, sep:str = ...) -> str:
    ...

def ForeCyan(*args, sep:str = ...) -> str:
    ...

def ForeWhite(*args, sep:str = ...) -> str:
    ...

def ForeLightBlack(*args, sep:str = ...) -> str:
    ...

def ForeLightRed(*args, sep:str = ...) -> str:
    ...

def ForeLightGreen(*args, sep:str = ...) -> str:
    ...

def ForeLightYellow(*args, sep:str = ...) -> str:
    ...

def ForeLightBlue(*args, sep:str = ...) -> str:
    ...

def ForeLightMagenta(*args, sep:str = ...) -> str:
    ...

def ForeLightCyan(*args, sep:str = ...) -> str:
    ...

def ForeLightWhite(*args, sep:str = ...) -> str:
    ...

def StartBlack() -> None:
    ...

def StartRed() -> None:
    ...

def StartGreen() -> None:
    ...

def StartYellow() -> None:
    ...

def StartBlue() -> None:
    ...

def StartMagenta() -> None:
    ...

def StartCyan() -> None:
    ...

def StartWhite() -> None:
    ...

def StartLightBlack() -> None:
    ...

def StartLightRed() -> None:
    ...

def StartLightGreen() -> None:
    ...

def StartLightYellow() -> None:
    ...

def StartLightBlue() -> None:
    ...

def StartLightMagenta() -> None:
    ...

def StartLightCyan() -> None:
    ...

def StartLightWhite() -> None:
    ...
