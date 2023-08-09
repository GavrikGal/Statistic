import abc
from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pathlib
import re
from typing import List, Union

from .utils import make_unique_frequency_list, determine_max_y_tick


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


@dataclass
class Line:
    color: str = 'gray'
    style: str = '-'
    width: float = 1.


class BaseRadarPlotter(abc.ABC):
    """Класс построителя круговых диаграмм по подготовленным данным о зонах R2 в RadarData"""

    def __init__(self, radar_data: BaseRadarData, radar_data2: BaseRadarData = None,
                 radar_data_list: List[BaseRadarData] = None, max_y_tick: int = None):
        """
        Подготавливает графики с зонами R2 или Уровнями сигнала к отображению

        :param radar_data: данные о R2 по углам
        :param radar_data2: второй набор данных о R2 для сравнения с первым
        """
        self.rdata: BaseRadarData = radar_data
        self.rdata2: BaseRadarData = radar_data2        # todo: избавиться от rdata2, заменив на список данных

        self.rdata_list: List[BaseRadarData] = []
        if radar_data_list is not None and len(radar_data_list) > 0:
            self.rdata_list = radar_data_list
        else:
            self.rdata_list.append(self.rdata)

        self.data_list: List[pd.DataFrame] = [rdata.data for rdata in self.rdata_list]

        self.frequency_list: List[float] = sorted(make_unique_frequency_list(self.data_list))

        if max_y_tick is not None:
            self.max_y_tick = max_y_tick
        else:
            self.max_y_tick = determine_max_y_tick(self.data_list)

        # Настройки стилей линий зависят от наличия второго набора данных
        self.line1: Line = Line('r', '-', 1.6)
        self.line2: Union[None, Line] = None
        if self.rdata2 is not None:
            self.line1 = Line('b', '--', 1.1)
            self.line2 = Line('r', '-', 1.6)

        # Список настроек стилей линий todo: стек для хранения линий, больше дефолтных настроек линий
        self.lines: List[Line] = [
            Line('b', '--', 1.1),
            Line('r', '-', 1.6)
        ]

        # Построение графиков переопределенным методом
        self.make_plot()

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
            plt.savefig(self.rdata.dir.joinpath('plot.png'), dpi=400)
        else:
            plt.savefig(pathlib.Path(path), dpi=400)
