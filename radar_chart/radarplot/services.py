import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pathlib
from collections import namedtuple

from .utils.base import BaseRadarData


class RadarDataR2(BaseRadarData):
    """Класс данных для круговых диаграмм зон R2 по углам"""

    def __init__(self, dir_path: str):
        """
        Подготавливает данные о зонах R2 (на всех углах измерения) для отображения их на круговых диаграммах

        :param dir_path: путь к папке со списком файлов данных
        """
        BaseRadarData.__init__(self, dir_path)

    def _make_data(self) -> pd.Series:
        """
        Читает имя каждого файла из списка self.files парсит в нем угол, на котором проводились измерения, и
        результат рассчитанной зоны R2. Из этих данных формирует ДатаСерию для всех положений (углов) измерений

        :return: ДатаСерия с углами, в качестве индексов, и R2, в качестве значений
        """

        data_set = {}
        # Перебрать названия всех файлов папки и выбрать из них угол,
        # на котором проводились измерения, и радиус зоны R2
        for filename in self.files:
            angle = self._get_angle_from_filename(filename)
            r2 = self._get_r2_from_filename(filename)
            data_set[np.deg2rad(angle)] = r2

        # Создать объект данных pandas и отсортировать его
        data = pd.Series(data_set).sort_index()

        # Добавить в конец ДатаСерии данные начальной точки, чтобы график замкнулся
        data = pd.concat([data, data[:0]])

        return data


class RadarPlotter(object):
    """Класс построителя круговых диаграмм по подготовленным данным о зонах R2 в RadarData"""

    def __init__(self, radar_data: RadarDataR2, radar_data2: RadarDataR2 = None, y_max: int = None):
        """
        Подготавливает графики с зонами R2 к отображению

        :param radar_data: данные о R2 по углам
        :param radar_data2: второй набор данных о R2 для сравнения с первым
        """
        self.rdata: RadarDataR2 = radar_data
        self.rdata2: RadarDataR2 = radar_data2

        # Настройки стилей линий зависят от наличия второго набора данных
        Line = namedtuple('Properties', 'color style width')
        if self.rdata2 is not None:
            line1 = Line('b', '--', 1.1)
            line2 = Line('r', '-', 1.6)
        else:
            line1 = Line('r', '-', 1.6)
            line2 = None

        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

        # Настройка максимальной величины оси уровней R2
        if y_max is not None:
            plt.ylim((0, y_max))

        # Построение линнии первых данных
        ax.plot(self.rdata.data, color=line1.color, linewidth=line1.width, linestyle=line1.style)

        # Если есть данные для сравнения, то отобразить и их
        if self.rdata2 is not None:
            ax.plot(self.rdata2.data, color=line2.color, linewidth=line2.width, linestyle=line2.style)

    @staticmethod
    def show():
        plt.show()

    def save(self, path: str = None):
        if path is None:
            plt.savefig(self.rdata.dir.joinpath('plot.png'), dpi=300)
        else:
            plt.savefig(pathlib.Path(path), dpi=300)
