import abc


import matplotlib.pyplot as plt
import pandas as pd
import pathlib
from typing import List

from ..utils import make_unique_frequency_list, determine_max_y_tick, Line
from ..radar_data.base import BaseRadarData


DEFAULT_LINE_STYLES = [
    Line('royalblue', '--', 1.1),
    Line('tomato', '-', 1.6),
    Line('forestgreen', ':', 1)
]


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
        if line_styles is None:
            self.lines = DEFAULT_LINE_STYLES
        else:
            self.lines = line_styles

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
