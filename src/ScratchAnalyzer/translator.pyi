import json5
from .Scratch import Language


class WrappedTranslator(object):
    translator: dict[str, str]
    meta: dict[str, str]
    
    def __init__(self, translator: dict[str, str], meta: dict[str, str]):
        ...

    def __getattr__(self, item: str) -> str:
        ...

def load_translator(language: Language) -> WrappedTranslator:
    ...