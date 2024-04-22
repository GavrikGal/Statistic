import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from typing import List

from radar_chart.radarplot.plotter.base import BaseRadarPlotter
from ..radar_data import RadarDataR2
from ..utils import Line


class RadarR2Plotter(BaseRadarPlotter):
    """Класс построителя круговых диаграмм по подготовленным данным о зонах R2 в RadarData"""

    def __init__(self, radar_data_list: List[RadarDataR2] = None, max_y_tick: int = None,
                 line_styles: List[Line] = None):
        """
        Подготавливает графики с зонами R2 к отображению

        :param radar_data_list: список подготовленных данных R2 по углам для сравнения
        :param max_y_tick: Предел шкалы зон R2
        """
        BaseRadarPlotter.__init__(self, radar_data_list, max_y_tick, line_styles=line_styles)
        self.make_plot()

    # def calc_lower_r2(self, data: pd.Series) -> pd.Series:
    #     """Вычисляет нижний уровень неопределенности зоны R2"""
    #     min_data = []
    #     for r2 in data:
    #         if r2 <= 10:
    #             min_data.append(r2 - 1)
    #         else:
    #             min_data.append(r2 - 5)
    #     return pd.Series(min_data)

    def make_plot(self):
        """Из данных о зонах R2 на различных углах подготавливает круговые диаграммы"""
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

        # Настройка максимальной величины оси уровней R2
        if self.max_y_tick is not None:
            plt.ylim((0, self.max_y_tick))

        # Построение линнии данных
        for i_rdata, rdata in enumerate(self.rdata_list):

            # Вычислить нижние уровни неопределённости зоны R2
            # min_data = self.calc_lower_r2(rdata.data)

            # Построить линии графика
            ax.plot(rdata.data.index.values, rdata.data['main'], color=self.lines[i_rdata].color,
                    linewidth=self.lines[i_rdata].width,
                    linestyle=self.lines[i_rdata].style,
                    alpha=self.lines[i_rdata].alpha, zorder=i_rdata)

            # Заполнить неопределенность заливкой
            if 'lower' in rdata.data.columns:
                ax.fill_between(rdata.data.index.values, rdata.data['main'], y2=rdata.data['lower'],
                                color=self.lines[i_rdata].color,
                                linewidth=0.5,
                                linestyle=self.lines[i_rdata].style,
                                alpha=self.lines[i_rdata].alpha-0.5, zorder=i_rdata)
            if 'upper' in rdata.data.columns:
                ax.fill_between(rdata.data.index.values, rdata.data['main'], y2=rdata.data['upper'],
                                color=self.lines[i_rdata].color,
                                linewidth=0.5,
                                linestyle=self.lines[i_rdata].style,
                                alpha=self.lines[i_rdata].alpha-0.5, zorder=i_rdata)

        # Настройка сетки графика
        ax.set_yticks(np.arange(0, self.max_y_tick, 5))
        ax.set_yticks(np.arange(0, self.max_y_tick, 1), minor=True)
        ax.grid(which='minor', color='gray', linewidth=0.3, alpha=0.2)
        ax.grid(which='major', color='dimgray', linewidth=0.4, alpha=0.5)
