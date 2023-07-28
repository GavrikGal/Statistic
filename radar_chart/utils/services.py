import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pathlib
import re
from typing import List, Tuple
from collections import namedtuple


class RadarData(object):
    """Класс данных для круговых диаграмм зон R2 по углам"""

    def __init__(self, dir_path: str):
        """
        Подготавливает данные о зонах R2 (на всех углах измерения) для отображения их на круговых диаграммах

        :param dir_path: путь к папке со списком файлов данных
        """
        self.dir: pathlib.Path = pathlib.Path(dir_path)
        self.files: List[str] = self._read_filenames()
        self.data: pd.Series = self._make_data()

    def _read_filenames(self) -> List[str]:
        """
        Прочитать список файлов из заданной папки

        :return: список текстовых файлов
        """
        file_list = [file.name for file in self.dir.iterdir() if file.is_file() and file.name.endswith('.txt')]
        return file_list

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
            angle, r2 = self._get_angle_and_r2_from_filename(filename)
            data_set[np.deg2rad(angle)] = r2

        # Создать объект данных pandas и отсортировать его
        data = pd.Series(data_set).sort_index()

        # Добавить в конец ДатаСерии данные начальной точки, чтобы график замкнулся
        data = pd.concat([data, data[:0]])

        return data

    @staticmethod
    def _get_angle_and_r2_from_filename(filename: str) -> Tuple[float, float]:
        """
        Парсит имя файла на угол, на котором проводились измерения, и результат рассчитанной зоны R2

        :param filename: имя файла
        :return: угол, R2
        """
        angle = float(re.findall(r'\((\d+)\)', filename)[0])
        r2 = float(re.findall(r'\) (\d+)', filename)[0])
        return angle, r2


class RadarPlotter(object):
    """Класс построителя круговых диаграмм по подготовленным данным о зонах R2 в RadarData"""

    def __init__(self, radar_data: RadarData, radar_data2: RadarData = None, y_max: int = None):
        """
        Подготавливает графики с зонами R2 к отображению

        :param radar_data: данные о R2 по углам
        :param radar_data2: второй набор данных о R2 для сравнения с первым
        """
        self.rdata: RadarData = radar_data
        self.rdata2: RadarData = radar_data2

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

        # Если есть данные для сравнения, то сравнить их
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
