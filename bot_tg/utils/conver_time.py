from datetime import datetime


async def convert_datetime(date: str, format_from: str = '%Y-%m-%dT%H:%M:%S.%f', format_to: str = '%H:%M - %d.%m.%y'):
    """Переконвертация строки времени"""
    return datetime.strptime(date, format_from).strftime(format_to)
