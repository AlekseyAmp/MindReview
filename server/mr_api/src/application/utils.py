import os
import shutil
from datetime import datetime
from pathlib import Path

import pytz
from openpyxl.worksheet.worksheet import Worksheet
from passlib.context import CryptContext

from fastapi import UploadFile

from src.application.constants import FileConstants


# Утилиты для работы со временем
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


def datetime_to_json(dt: datetime) -> str:
    """
    Преобразует объект даты и времени в строку в формате JSON.

    :param dt: Объект даты и времени.

    :return: Строка в формате JSON.
    """
    return dt.strftime('%Y-%m-%d %H:%M:%S')


# Утилиты для валдиации данных
def validate_non_empty_fields(data: dict) -> str | None:
    """
    Проверяет, что все значения в переданном словаре
    не являются пустыми.

    Если хотя бы одно значение пустое или содержит
    только пробельные символы,
    возвращается имя первого обнаруженного пустого поля.

    :param data: Словарь с данными для проверки.

    :return: Имя первого обнаруженного пустого поля или None,
    если все поля заполнены.
    """
    def check_value(val) -> bool:
        if isinstance(val, str) and not val.strip():
            return True
        elif isinstance(val, list):
            if not val or any(
                not item
                or not str(item).strip()
                for item in val
            ):
                return True
        elif isinstance(val, dict):
            if validate_non_empty_fields(val):
                return True
        elif not val:
            return True
        return False

    for field_name, value in data.items():
        if check_value(value):
            return field_name


# Утилиты для работы с файлами
def is_not_valid_file_format(filename: str) -> bool:
    """
    Проверяет формат файла по его расширению.

    Проверяет расширение указанного файла и сравнивает его
    с разрешенными форматами.
    Если расширение файла не соответствует ни одному из разрешенных форматов,
    возвращает True

    :param filename: Имя файла или путь к файлу для проверки формата.

    :return bool: True, если формат невалидный, иначе False
    """
    ext = Path(filename).suffix.lower()
    if ext in FileConstants.ALLOWED_FORMATS:
        return False

    return True


def is_file_empty(ws: Worksheet) -> bool:
    """
    Проверяет, является ли файл пустым.

    :param ws: Рабочий лист (Worksheet) Excel для проверки.

    :return: True, если файл пустой, иначе False.
    """
    for row in ws.iter_rows(values_only=True):
        if any(str(cell).strip() for cell in row if cell):
            return False

    return True


def get_file_num_rows(ws: Worksheet) -> int:
    """
    Возвращает количество строк в рабочем листе Excel.

    Подсчитывает количество заполненных строк в указанном
    рабочем листе Excel и возвращает это значение.

    :param ws: Рабочий лист (Worksheet) Excel для подсчета строк.

    :return: Количество строк в рабочем листе.
    """
    num_rows = ws.max_row
    return num_rows


def save_file(file: UploadFile, user_id: str) -> str:
    """
    Сохраняет загруженный файл в директории пользователя.

    :param file: Объект загруженного файла.
    :param user_id: Идентификатор пользователя.

    :return: Путь к сохраненному файлу.
    """

    # Создаем папку для пользователя, если ее нет
    user_dir = os.path.join(FileConstants.UPLOAD_DIR, str(user_id))
    os.makedirs(user_dir, exist_ok=True)

    # Полный путь к файлу
    file_path = os.path.join(user_dir, file.filename)

    # Проверяем, существует ли файл с таким именем
    if os.path.exists(file_path):
        # Разделяем имя файла и расширение
        name, ext = os.path.splitext(file.filename)
        index = 1
        # Ищем первый свободный индекс для добавления к имени файла
        while os.path.exists(os.path.join(user_dir, f"{name} ({index}){ext}")):
            index += 1
        # Формируем новое имя файла с индексом
        file_path = os.path.join(user_dir, f"{name} ({index}){ext}")

    # Сохраняем файл
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_path


# Утилиты для работы с паролем
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
