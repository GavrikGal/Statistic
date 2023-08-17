import abc


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pathlib
import re
from typing import List, Union

from .utils import make_unique_frequency_list, determine_max_y_tick, Line


DEFAULT_LINE_STYLES = [
    Line('royalblue', '--', 1.1),
    Line('tomato', '-', 1.6)
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


class BaseRadarPlotter(abc.ABC):
    """Класс построителя круговых диаграмм по подготовленным данным о зонах R2 в RadarData"""

    def __init__(self, radar_data_list: List[BaseRadarData], max_y_tick: int = None,
                 line_styles: List[Line] = DEFAULT_LINE_STYLES):
        """
        Подготавливает графики с зонами R2 или Уровнями сигнала к отображению

        :param radar_data_list: список данных R2 по углам для сравнения
        :param max_y_tick:
        :param line_styles:
        """

        self.rdata_list: List[BaseRadarData] = radar_data_list
        self.data_list: List[pd.DataFrame] = [rdata.data for rdata in self.rdata_list]
        self.frequency_list: List[float] = sorted(make_unique_frequency_list(self.data_list))

        if max_y_tick is not None:
            self.max_y_tick = max_y_tick
        else:
            self.max_y_tick = determine_max_y_tick(self.data_list)

        # Список настроек стилей линий todo: стек для хранения линий, больше дефолтных настроек линий
        self.lines = line_styles

        # # Построение графиков переопределенным методом
        # self.make_plot()

    @abc.abstractmethod
    def make_plot(self):
        """Из данных о зонах R2 или Уровней сигналов в self.rdata должен подготовить графики для отображения"""

    @staticmethod
    def show():
        """Отобразить график"""
        plt.show()

    def save(self, path: str = None):
        """сохранить график"""
        if path is None:
            plt.savefig(self.rdata_list[0].dir.joinpath(' [график].png'), dpi=400)
        else:
            plt.savefig(pathlib.Path(path), dpi=400)
