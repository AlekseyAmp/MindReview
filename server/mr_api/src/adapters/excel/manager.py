import typing
from dataclasses import dataclass

from openpyxl import load_workbook
from openpyxl.worksheet.worksheet import Worksheet

from src.application.review import interfaces


@dataclass
class ExcelManager(interfaces.ExcelManager):
    def load_data(self, file: typing.BinaryIO) -> Worksheet:
        """
        Загружает и возвращает активный лист из Excel файла.

        :param file: Файл Excel для загрузки.

        :return: Активный лист Excel.
        """

        wb = load_workbook(file)
        ws = wb.active
        return ws
