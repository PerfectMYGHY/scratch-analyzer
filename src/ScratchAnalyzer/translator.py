import json


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
    with open(f"translator.{language.lower()}.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return WrappedTranslator(data)