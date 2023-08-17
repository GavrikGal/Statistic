import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from typing import List

from ..base import BaseRadarPlotter, Line
# from radar_chart.radarplot.radar_data.levels_data import RadarDataLevels
from ..radar_data import RadarDataLevels


class RadarLevelsPlotter(BaseRadarPlotter):
    """Класс построителя круговых диаграмм по подготовленным данным об Уровнях сигналов в RadarData"""

    def __init__(self, radar_data: RadarDataLevels, radar_data2: RadarDataLevels = None,
                 radar_data_list: List[RadarDataLevels] = None, max_y_tick: int = None,
                 col_count: int = 4):
        """
        Подготавливает графики с Уровнями сигналов к отображению

        :param radar_data: данные об уровнях сигналов по углам первого измерения
        :param radar_data2: данные об уровнях сигналов по углам второго измерения для отображения на графиках
        с первыми данными
        :param max_y_tick: Предел шкалы уровней сигналов
        :param col_count: Количество колонок с графиками
        """
        self.col_count: int = col_count
        self.row_count: int = 4

        self.angels: List[float] = []

        BaseRadarPlotter.__init__(self, radar_data, radar_data2, radar_data_list, max_y_tick)

    def make_plot(self):
        """Из данных об Уровнях сигнала на различных угла подготавливает круговые диаграммы для каждой частоты"""

        # Список углов, на которых проводились измерения надо сохранить в self.angels,
        self.angels = self.rdata.data.index.values
        # если углы первой и второй выборки отличаются, то надо выкинуть ошибку  todo

        # Рассчет количества графиков по вертикали и горизонтали
        self.row_count = math.ceil(len(self.frequency_list) / self.col_count)

        # Размер холста
        plt.figure(layout='constrained', figsize=(self.col_count * 2.5, self.row_count * 3))

        # Для каждой частоты данных
        for frequency in self.frequency_list:
            axes = plt.subplot(self.row_count, self.col_count,
                               pd.Index(self.frequency_list).get_loc(frequency) + 1, projection='polar')

            # Настройка шкалы уровней текущего графика
            plt.ylim((0, self.max_y_tick))

            # Общие настройки коэффициентов графиков
            min_color_ratio = 10
            min_width_ratio = -10

            # Название текущего графика
            plt.title(f"{frequency} МГц", loc='center')

            for i_rdata, rdata in enumerate(self.rdata_list):
                if frequency in rdata.data.columns.values:
                    data = rdata.data[frequency]

                    # Настройка цвет и ширины бара
                    color_ratio_s = (data - min_color_ratio) / (self.max_y_tick - min_color_ratio)
                    color_ratio_n = (rdata.noise[frequency] - min_color_ratio) / (self.max_y_tick - min_color_ratio)
                    colors_s = plt.cm.jet(color_ratio_s)
                    colors_n = plt.cm.jet(color_ratio_n)

                    # todo: навести порядок на рефайкторинге
                    width_ratio = (data - min_width_ratio) / (self.max_y_tick - min_width_ratio)
                    if self.rdata2 is not None:
                        signal_max = max(self.rdata.data.max().max(), self.rdata2.data.max().max())     # todo: найти максимум у сигналов data_list
                        width_ratio = (data - min_width_ratio) / (signal_max - min_width_ratio)
                        width_ratio *= 0.9
                    width = (2 * np.pi / data.shape[0]) * width_ratio

                    # Построение графика шума
                    axes.bar(data.index.values, rdata.noise[frequency], width=0.81, edgecolor='dimgray', color=colors_n,
                             linewidth=0.6, zorder=1, alpha=0.4)
                    # Если есть только одна выборка, то бары сигнала во всю ширину сектора, иначе вполовину, сместить
                    # и покрасить ребра в различимые цвета
                    offset = 0
                    width_offset_ratio = 1

                    # todo: убрать настройки линий из этого метода при рефакторинге
                    self.lines = [
                        Line('mediumblue', '-', 1),
                        Line('firebrick', '-', 1)
                    ]

                    # todo: убрать
                    if len(self.rdata_list) == 1:
                        self.line1.color = 'gray'
                        self.line1.width = 0.4

                    # todo: переделать расчет ширины лепестков и их смещение от количества выборок (сделать функцию)
                    if len(self.rdata_list) > 1:
                        width_offset_ratio = 0.8
                        offset = 2 * (((width * width_offset_ratio) / 2) - ((width * width_offset_ratio) - (width / 2)))

                    # Построить график сигнала
                    axes.bar(data.index.values-offset/2+(i_rdata*offset), data,
                             width=width*width_offset_ratio,
                             edgecolor=self.lines[i_rdata].color, color=colors_s,
                             linewidth=self.lines[i_rdata].width, zorder=5, alpha=0.8)

            # if frequency in self.frequency_list:
            #     radar_data = self.rdata.radar_data[frequency]
            #
            #     # Настройка цвет и ширины бара
            #     color_ratio_s = (radar_data - min_color_ratio) / (self.max_y_tick - min_color_ratio)
            #     color_ratio_n = (self.rdata.noise[frequency] - min_color_ratio) / (self.max_y_tick - min_color_ratio)
            #     colors_s = plt.cm.jet(color_ratio_s)
            #     colors_n = plt.cm.jet(color_ratio_n)
            #
            #     # todo: навести порядок на рефайкторинге
            #     width_ratio = (radar_data - min_width_ratio) / (self.max_y_tick - min_width_ratio)
            #     if self.rdata2 is not None:
            #         signal_max = max(self.rdata.radar_data.max().max(), self.rdata2.radar_data.max().max())
            #         width_ratio = (radar_data - min_width_ratio) / (signal_max - min_width_ratio)
            #         width_ratio *= 0.9
            #     width = (2 * np.pi / radar_data.shape[0]) * width_ratio
            #
            #     # Построение графика шума
            #     axes.bar(radar_data.index.values, self.rdata.noise[frequency], width=0.81, edgecolor='dimgray', color=colors_n,
            #              linewidth=0.6, zorder=1, alpha=0.8)
            #     # Если есть только одна выборка, то бары сигнала во всю ширину сектора, иначе вполовину, сместить
            #     # и покрасить ребра в различимые цвета
            #     offset1 = 0
            #     width_offset_ratio = 1
            #
            #     # todo: убрать настройки линий из этого метода при рефакторинге
            #     self.line1 = Line('mediumblue', '-', 1)
            #     self.line2 = Line('firebrick', '-', 1)
            #
            #     if self.rdata2 is None:
            #         self.line1.color = 'gray'
            #         self.line1.width = 0.4
            #
            #     if self.rdata2 is not None:
            #         width_offset_ratio = 0.8
            #         offset1 = -(((width * width_offset_ratio) / 2) - ((width * width_offset_ratio) - (width / 2)))
            #
            #     # Построить график сигнала
            #     axes.bar(radar_data.index.values+offset1, radar_data,
            #              width=width*width_offset_ratio,
            #              edgecolor=self.line1.color, color=colors_s,
            #              linewidth=self.line1.width, zorder=5, alpha=0.8)

            # Если есть вторая выборка, построить дня нее график
            # if self.rdata2 is not None:
            #     if frequency in self.rdata2.radar_data.columns.values:
            #         radar_data = self.rdata2.radar_data[frequency]
            #
            #         # Настройка цвет и ширины бара
            #         color_ratio_s = (radar_data - min_color_ratio) / (self.max_y_tick - min_color_ratio)
            #         color_ratio_n = (self.rdata2.noise[frequency] - min_color_ratio) / (self.max_y_tick -
            #                                                                             min_color_ratio)
            #         colors_s = plt.cm.jet(color_ratio_s)
            #         colors_n = plt.cm.jet(color_ratio_n)
            #
            #         # todo: навести порядок на рефайкторинге
            #         signal_max = max(self.rdata.radar_data.max().max(), self.rdata2.radar_data.max().max())
            #         width_ratio = (radar_data - min_width_ratio) / (signal_max - min_width_ratio)
            #         width_ratio *= 0.9
            #         width = (2 * np.pi / radar_data.shape[0]) * width_ratio
            #
            #         # Построение графика шума
            #         if frequency not in self.rdata.radar_data.columns.values:
            #             axes.bar(radar_data.index.values, self.rdata2.noise[frequency], width=0.81, edgecolor='dimgray', color=colors_n,
            #                      linewidth=0.6, zorder=1)
            #
            #         # Если есть только одна выборка, то бары сигнала во всю ширину сектора, иначе вполовину, сместить
            #         # и покрасить ребра в различимые цвета todo
            #         offset1 = 0
            #         width_offset_ratio = 1
            #         if self.rdata2 is not None:
            #             width_offset_ratio = 0.8
            #             offset1 = (((width * width_offset_ratio) / 2) - ((width * width_offset_ratio) - (width / 2)))
            #
            #         # Построить график сигнала
            #         axes.bar(radar_data.index.values+offset1, radar_data,
            #                  width=width*width_offset_ratio,
            #                  edgecolor=self.line2.color, color=colors_s,
            #                  linewidth=self.line2.width, zorder=6, alpha=0.8)

            # Настройка сетки графика
            axes.tick_params(axis='both', which='major', labelsize=8)
            axes.set_yticks(np.arange(0, self.max_y_tick, 10))
            axes.set_yticks(np.arange(0, self.max_y_tick, 2), minor=True)
            axes.grid(which='minor', color='lightgray', linewidth=0.3, alpha=0.3)
            axes.grid(which='major', linewidth=0.4, alpha=0.9)

    # def determine_max_y_tick(self, df: pd.DataFrame, df2: pd.DataFrame = None) -> None:
    #     """
    #     Определение и установка максимального предела шкалы графика уровней (self.y_max) кратным 10 исходя
    #     из максимальных уровней данных в выборке(выборках)
    #     :param df: первая выборка данных
    #     :param df2: вторая выборка данных
    #     """
    #     y_max = df.max().max()
    #     if df2 is not None:
    #         y_max2 = df2.max().max()
    #         y_max = max(y_max, y_max2)
    #     self.y_max = math.ceil(y_max / 10) * 10


