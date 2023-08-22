import abc
import numpy as np
import pandas as pd
import pathlib
import re
from typing import List, Union

from ..utils import Line


DEFAULT_LINE_STYLES = [
    Line('royalblue', '--', 1.1),
    Line('tomato', '-', 1.6),
    Line('forestgreen', ':', 1)
]


class BaseRadarData(abc.ABC):
    """Базовый Класс данных для круговых диаграмм зон R2 по углам"""

    def __init__(self, dir_path: str):
        """
        Подготавливает данные о зонах R2 (на всех углах измерения) для отображения их на круговых диаграммах

        :param dir_path: путь к папке со списком файлов данных
        """
        self.dir: pathlib.Path = pathlib.Path(dir_path)
        self.files: List[str] = self.read_filenames()
        self.noise: Union[None, pd.DataFrame] = None
        self.data: Union[pd.Series, pd.DataFrame] = self.make_data()

    def read_filenames(self) -> List[str]:
        """
        Прочитать список файлов из заданной папки

        :return: список текстовых файлов
        """
        file_list = [file.name for file in self.dir.iterdir() if file.is_file() and file.name.endswith('.txt')]
        return file_list

    @abc.abstractmethod
    def make_data(self) -> Union[pd.Series, pd.DataFrame]:
        """
        Должен читать имя каждого файла из списка self.files, парсить в нем угол, на котором проводились
        измерения, и, в зависимости от необходимости, парсит либо результат рассчитанной зоны R2,
        либо результаты измеренных уровней. Из этих данных формирует набор данный pandas
        для всех положений (углов) измерений

        :return: Набор данных pandas.Series или pandas.DataFrame с углами, в качестве индексов,
        и R2 или Уровней, в качестве значений
        """

    @staticmethod
    def get_angle_from_filename(filename: str) -> float:
        """
        Парсит имя файла на угол, на котором проводились измерения, и результат рассчитанной зоны R2

        :param filename: имя файла
        :return: угол, R2
        """
        angle = np.deg2rad(float(re.findall(r'\((\d+)\)', filename)[0]))
        return angle

    @staticmethod
    def get_r2_from_filename(filename: str) -> float:
        """
        Парсит имя файла на угол, на котором проводились измерения, и результат рассчитанной зоны R2

        :param filename: имя файла
        :return: угол, R2
        """
        r2 = float(re.findall(r'\) (\d+)', filename)[0])
        return r2
