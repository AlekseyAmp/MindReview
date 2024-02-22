from datetime import datetime

import pytz
from passlib.context import CryptContext

from src.application import exceptions


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


def validate_non_empty_fields(data: dict) -> None:
    """
    Проверяет, что все значения в переданном словаре не пустые.

    Если хотя бы одно значение пустое или содержит
    только пробельные символы,
    возбуждается исключение EmptyFieldException.

    :param data: Словарь с данными для проверки.
    :raises EmptyFieldException: Если хотя бы одно значение пустое
    или содержит только пробельные символы.
    """
    for field_name, value in data.items():
        if not value or not value.strip():
            exceptions.EmptyFieldException(field_name)


# Контекст для хеширования и проверки паролей с использованием bcrypt.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Хеширует переданный пароль с использованием bcrypt.

    :param password: Пароль для хеширования.
    :return: Хеш пароля.
    """
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Проверяет, соответствует ли переданный пароль его хешу.

    :param password: Пароль для проверки.
    :param hashed_password: Хеш пароля для сравнения.
    :return: True, если пароль соответствует хешу, иначе False.
    """
    return pwd_context.verify(password, hashed_password)
