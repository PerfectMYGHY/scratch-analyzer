import json5
from .public import assets_root_path


class WrappedTranslator(object):
    """
    翻译器数据包装，可直接用属性获取翻译格式化数据
    """
    def __init__(self, translator, meta):
        self.translator = translator
        self.meta = meta
    
    def __getattr__(self, item):
        translator = super().__getattribute__('translator')
        meta = super().__getattribute__('meta')
        # 先在字典属性translator中查找
        if item in translator:
            return translator[item]
        elif item in meta: # 再先在字典属性meta中查找
            return meta[item]
        else:
            # 如果找不到，调用父类的__getattribute__方法
            return super().__getattribute__(item)

def load_translator(language):
    """
    加载指定语言的翻译器数据
    """
    with open(assets_root_path / f"translator.{language.lower()}.jsonc", "r", encoding="utf-8") as file:
        main_data = json5.load(file)
    with open(assets_root_path / f"translator.meta.{language.lower()}.jsonc", "r", encoding="utf-8") as file:
        meta_data = json5.load(file)
    return WrappedTranslator(main_data, meta_data)