async def suffix_text(value: int, one_value, some_value, many_value):
    result = ''
    if not value:
        return result

    last = abs(value) % 10
    if int(last) == 1 and not value == 11:
        result = f'{int(value)} {one_value}'
    elif 1 < last < 5 and not 11 < value < 15:
        result = f'{int(value)} {some_value}'
    else:
        result = f'{int(value)} {many_value}'

    if value < 0:
        result = "-" + result
    return result


async def get_str_time(k: int) -> str:
    """250 -> '4 часа 10 минут' """
    h = k // 60
    m = k % 60
    hour = await suffix_text(h, 'час', 'часа', 'часов')
    minute = await suffix_text(m, 'минута', 'минуты', 'минут')
    return f'{hour} {minute}'
