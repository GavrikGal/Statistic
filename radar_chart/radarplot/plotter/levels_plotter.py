import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from typing import List

from radar_chart.radarplot.plotter.base import BaseRadarPlotter, Line
from ..radar_data import RadarDataLevels


class RadarLevelsPlotter(BaseRadarPlotter):
    """Класс построителя круговых диаграмм по подготовленным данным об Уровнях сигналов в RadarData"""

    def __init__(self, radar_data_list: List[RadarDataLevels],
                 max_y_tick: int = None, col_count: int = 4):
        """
        Подготавливает графики с Уровнями сигналов к отображению

        :param radar_data_list: список подготовленных данных с уровнями по углам
        для сравнения
        :param max_y_tick: Предел шкалы уровней сигналов
        :param col_count: Количество колонок с графиками
        """

        self.angels: List[float] = []

        line_styles = [
            Line('firebrick', '-', 1),
            Line('mediumblue', '-', 1),
            Line('forestgreen', ':', 1),
            Line('darkorange', ':', 1),
        ]

        BaseRadarPlotter.__init__(self, radar_data_list,
                                  max_y_tick, line_styles=line_styles)

        self.col_count: int = col_count
        # Рассчет количества графиков по вертикали и горизонтали
        self.row_count = math.ceil(len(self.frequency_list) / self.col_count)

        self.make_plot()

    def make_plot(self):
        """Из данных об Уровнях сигнала на различных угла подготавливает круговые диаграммы для каждой частоты"""

        # Список углов, на которых проводились измерения надо сохранить в self.angels,
        # todo: если углы первой и второй выборки отличаются, то надо выкинуть ошибку
        self.angels = self.data_list[0].index.values

        # Размер холста
        plt.figure(layout='constrained', figsize=(self.col_count * 2.5, self.row_count * 3))

        # Для каждой частоты данных
        for frequency in self.frequency_list:
            axes = plt.subplot(self.row_count, self.col_count,
                               pd.Index(self.frequency_list).get_loc(frequency) + 1, projection='polar')

            # Настройка шкалы уровней текущего графика
            plt.ylim((0, self.max_y_tick))

            # Название текущего графика
            plt.title(f"{frequency} МГц", loc='center')

            # При построении графиков используется обратный порядок построения,
            # чтобы график с последними данными был сверху
            for i_rdata, rdata in enumerate(reversed(self.rdata_list)):
                if frequency in rdata.data.columns.values:
                    signal = rdata.data[frequency]
                    noise = rdata.noise[frequency]

                    # Настройка цвета лепестков
                    min_color_factor = 10
                    color_signal_factors = (signal - min_color_factor) / (self.max_y_tick - min_color_factor)
                    color_noise_factors = (noise - min_color_factor) / (self.max_y_tick - min_color_factor)
                    signal_colors = plt.cm.jet(color_signal_factors)
                    noise_colors = plt.cm.jet(color_noise_factors)

                    # Настройка ширины лепестков
                    min_width_factor = -10
                    width_factors = (signal - min_width_factor) / (self.max_y_tick - min_width_factor)
                    segment_width = (2 * np.pi / signal.shape[0])
                    widths = segment_width * width_factors

                    # Построение графика шума
                    axes.bar(noise.index.values, noise, width=0.8, edgecolor='dimgray', color=noise_colors,
                             linewidth=0.6, zorder=3, alpha=0.5/len(self.rdata_list))

                    # Расчет ширины лепестков и их смещение от количества выборок
                    # todo: переделать (сделать функцию)
                    base_count_factor = 0.9
                    gap_between_bars = 0.05
                    if len(self.rdata_list) > 1:
                        width_count_factor = base_count_factor - 0.1 * (len(self.rdata_list) - 1) - gap_between_bars * base_count_factor
                        offset = (0.2 * width_count_factor) * widths
                        # todo: не работает offset = (((widths * width_count_factor) / 2) - ((widths * width_count_factor) - (widths / 2)))
                    else:
                        width_count_factor = base_count_factor
                        offset = 0

                    # Построить график сигнала
                    # todo: не работает segment_positions = signal.index.values - ((widths * width_count_factor) / 2 + offset)
                    segment_positions = signal.index.values + (i_rdata - ((len(self.rdata_list) - 1) / 2)) * offset
                    axes.bar(segment_positions, signal,
                             width=widths*width_count_factor,
                             edgecolor=self.lines[i_rdata].color, color=signal_colors,
                             linewidth=self.lines[i_rdata].width, zorder=10-i_rdata, alpha=0.8)

            # Настройка сетки графика
            axes.tick_params(axis='both', which='major', labelsize=8)
            axes.set_yticks(np.arange(0, self.max_y_tick, 10))
            axes.set_yticks(np.arange(0, self.max_y_tick, 2), minor=True)
            axes.grid(which='minor', color='lightgray', linewidth=0.3, alpha=0.3)
            axes.grid(which='major', linewidth=0.4, alpha=0.9)
