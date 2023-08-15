import math
import os

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from typing import List

from .base import BaseRadarData, BaseRadarPlotter


class RadarDataR2(BaseRadarData):
    """Класс данных для круговых диаграмм зон R2 по углам"""

    def __init__(self, dir_path: str):
        """
        Подготавливает данные о зонах R2 (на всех углах измерения) для отображения их на круговых диаграммах

        :param dir_path: путь к папке со списком файлов данных
        """
        BaseRadarData.__init__(self, dir_path)

    def make_data(self) -> pd.Series:
        """
        Читает имя каждого файла из списка self.files парсит в нем угол, на котором проводились измерения, и
        результат рассчитанной зоны R2. Из этих данных формирует ДатаСерию для всех положений (углов) измерений

        :return: ДатаСерия с углами, в качестве индексов, и R2, в качестве значений
        """

        data_set = {}
        # Перебрать названия всех файлов папки и выбрать из них угол,
        # на котором проводились измерения, и радиус зоны R2
        for filename in self.files:
            angle = self.get_angle_from_filename(filename)
            r2 = self.get_r2_from_filename(filename)
            data_set[angle] = r2

        # Создать объект данных pandas и отсортировать его
        data = pd.Series(data_set).sort_index()

        # Добавить в конец ДатаСерии данные начальной точки, чтобы график замкнулся
        data = pd.concat([data, data[:0]])

        return data


class RadarR2Plotter(BaseRadarPlotter):
    """Класс построителя круговых диаграмм по подготовленным данным о зонах R2 в RadarData"""

    def __init__(self, radar_data: RadarDataR2, radar_data2: RadarDataR2 = None,
                 radar_data_list: List[RadarDataR2] = None, max_y_tick: int = None):
        """
        Подготавливает графики с зонами R2 к отображению

        :param radar_data: данные о R2 по углам
        :param radar_data2: второй набор данных о R2 для сравнения с первым
        :param max_y_tick: Предел шкалы зон R2
        """
        BaseRadarPlotter.__init__(self, radar_data, radar_data2, radar_data_list, max_y_tick)

    def calc_lower_r2(self, data: pd.Series) -> pd.Series:
        """Вычисляет нижний уровень неопределенности зоны R2"""
        min_data = []
        for r2 in data:
            if r2 < 10:
                min_data.append(r2 - 1)
            else:
                min_data.append(r2 - 5)
        return pd.Series(min_data)

    def make_plot(self):
        """Из данных о зонах R2 на различных углах подготавливает круговые диаграммы"""
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

        # Настройка максимальной величины оси уровней R2
        if self.max_y_tick is not None:
            plt.ylim((0, self.max_y_tick))

        # Построение линнии данных
        for i_rdata, rdata in enumerate(self.rdata_list):

            # Вычислить нижние уровни неопределённости зоны R2
            min_data = self.calc_lower_r2(rdata.data)

            # fill_between

            ax.plot(rdata.data, color=self.lines[i_rdata].color,
                    linewidth=self.lines[i_rdata].width,
                    linestyle=self.lines[i_rdata].style,
                    alpha=0.9, zorder=i_rdata)
            ax.fill_between(rdata.data.index.values, rdata.data, y2=min_data,
                            color=self.lines[i_rdata].color,
                            linewidth=0,
                            linestyle=self.lines[i_rdata].style,
                            alpha=0.5, zorder=i_rdata)

        # Если есть данные для сравнения, то отобразить и их
        # if self.rdata2 is not None:
        #     ax.plot(self.rdata2.data, color=self.line2.color,
        #             linewidth=self.line2.width, linestyle=self.line2.style)

        # # Построение линнии первых данных
        # ax.plot(self.rdata.data, color=self.line1.color,
        #         linewidth=self.line1.width, linestyle=self.line1.style)
        #
        # # Если есть данные для сравнения, то отобразить и их
        # if self.rdata2 is not None:
        #     ax.plot(self.rdata2.data, color=self.line2.color,
        #             linewidth=self.line2.width, linestyle=self.line2.style)

        # Настройка сетки графика
        ax.set_yticks(np.arange(0, self.max_y_tick, 5))
        ax.set_yticks(np.arange(0, self.max_y_tick, 1), minor=True)
        ax.grid(which='minor', color='gray', linewidth=0.3, alpha=0.2)
        ax.grid(which='major', color='dimgray', linewidth=0.4, alpha=0.5)
