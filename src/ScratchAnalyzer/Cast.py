def toCode(value):
    if isinstance(value, int) or isinstance(value, float):
        code = str(value)
    else:
        try:
            value = float(value)
            if int(value) == value:
                value = int(value)
            code = str(value) # 判断是否是合法的数字字符串
        except ValueError:
            code = f'"{value}"'
    return code