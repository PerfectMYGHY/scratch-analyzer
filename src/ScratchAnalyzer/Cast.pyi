from typing import Any
from .translator import WrappedTranslator


def toCode(value: Any, translator: WrappedTranslator) -> str:
    ...
