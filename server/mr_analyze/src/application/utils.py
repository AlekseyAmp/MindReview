from datetime import datetime

import pytz


def get_current_dt(timezone: str = None) -> datetime:
    """
    Возвращает текущую дату и время без миллисекунд в указанном часовом поясе.

    :param timezone: Строка с идентификатором часового пояса.
    Если не указан, будет использован часовой пояс по умолчанию.

    :return: Текущая дата и время без миллисекунд.
    """
    current_dt = datetime.now(pytz.timezone(timezone))
    current_dt = current_dt.replace(microsecond=0)
    return current_dt


def round_float(score: float) -> str:
    """
    Форматирует числовую оценку с округлением
    до двух знаков после запятой.

    :param score: Числовая оценка.

    :return: Отформатированная строка с числовой оценкой.
    """
    return "{:.2f}".format(score)
