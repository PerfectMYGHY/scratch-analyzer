import json5
from .public import assets_root_path


class WrappedTranslator(object):
    def __init__(self, translator):
        self.translator = translator
    def __getattr__(self, item):
        translator = super().__getattribute__('translator')
        # 先在字典属性translator中查找
        if item in translator:
            return translator[item]
        else:
            # 如果找不到，调用父类的__getattribute__方法
            return super().__getattribute__(item)

def load_translator(language):
    with open(assets_root_path / f"translator.{language.lower()}.json5", "r", encoding="utf-8") as file:
        data = json5.load(file)
    return WrappedTranslator(data)