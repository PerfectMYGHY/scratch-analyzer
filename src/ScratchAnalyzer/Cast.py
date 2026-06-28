from .translator import WrappedTranslator
import math


def toCode(value, translator: WrappedTranslator) -> str: # translator会根据不同目标语言给出不同的代码版本
    if isinstance(value, int) or isinstance(value, float): # 如果直接是数字类型
        code = str(value)
    else:
        try:
            value = float(value) # 对于字符串，先转换为float，这样能广泛识别
            if math.isinf(value): # 对无穷特殊处理
                if value > 0:
                    return translator.positive_infinity
                else:
                    return translator.negative_infinity
            if math.isnan(value):
                return translator.nan
            if value.is_integer(): # 这种判断方法不会引发OverflowError
                value = int(value) # 转换为整数类型
            code = str(value) # 将数字转换为字符串
        except ValueError: # 则代表内容就是字符串
            code = f'"{value}"'
    return code