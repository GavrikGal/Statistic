import math
import os
import typing
from collections import namedtuple

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from typing import List

from .base import BaseRadarData, BaseRadarPlotter


# class SignalLevel(object):
#     """Класс уровня сигнала и уровня шума измеренного в [dB] сигнала"""
#     def __init__(self, meas_signal: float, meas_noise: float = 0):
#         self.meas_signal = meas_signal
#         self.meas_noise = meas_noise
#         self.signal = meas_signal   # В дальнейшем можно провести тут уточнение уровня сигнала, если вычесть из него шум
#         self.noise = meas_noise
#
#     def __str__(self):
#         return str((self.signal, self.noise))


class RadarDataLevels(BaseRadarData):
    """Класс данных для круговых диаграмм уровней излучений, измеренных в различных
    направлениях от изделия"""

    def __init__(self, dir_path: str):
        """
        Подготавливае данные об уровнях излучений (на всех углах измерений) из папки dir_path
        для отображения их на круговых диаграммах
        :param dir_path: путь к папке со списком файлов данных
        """
        BaseRadarData.__init__(self, dir_path)

    def _read_frequency_set(self) -> List[float]:
        """
        Получить список всех частот, на которых обнаружены сигналы, из всех файлов с данными
        :return: список частот
        """

        frequency_set = set()
        # Прочитать все файлы с данными из папки self.dir и из каждого прочитать список частот
        for filename in self.files:
            frequencies = pd.read_csv(os.path.join(self.dir, filename), sep='\t', encoding='cp1251', usecols=[1],
                                      skiprows=1).values
            # Каджую частоту добавить в set, который обеспечивает уникальность частот
            for freq in frequencies:
                frequency_set.add(freq[0])

        # Сортируем и отдаем set преобразовав его в list
        frequency_list = list(sorted(frequency_set))
        return frequency_list

    def _make_data(self) -> pd.DataFrame:
        """
        Читает имя каждого файла из списка self.files парсит в нем угол, на котором проводились измерения,
        и измеренный уровень сигнала. Из этих данных формирует ДатаФрейм для всех положений (углов) измерений
        и для всех частот, на которых обраружены сигналы

        :return: ДатаСерия с углами, в качестве индексов, и уровнями сигнала, в качестве значений
        """

        # Получить список всех частот из всех файлов
        self.frequencies = self._read_frequency_set()

        # Инициировать DataFrame сигналов и шумов с частотами в качестве индексов
        signal_data = pd.DataFrame(index=np.array(self.frequencies))
        noise_data = pd.DataFrame(index=np.array(self.frequencies))

        # Перебрать все файлы и вычитать есть ли в них данные на тех частотах, список которых нашли ранее
        for filename in self.files:
            # получить величину угла из названия файла
            angle = self._get_angle_from_filename(filename)

            # прочитать данные частоты, уровня сигнала и шума из файла
            # частоты установить в качестве индексов DataFrame
            file_dataframe = pd.read_csv(os.path.join(self.dir, filename), sep='\t', encoding='cp1251',
                                         usecols=[1, 2, 3], skiprows=2, index_col=0, names=['freq', 'signal', 'noise'])

            # заполнить ДатаФреймы сигналов и шумов
            signals = file_dataframe['signal']
            noises = file_dataframe['noise']
            signal_data[angle] = signals
            noise_data[angle] = noises

        # Пересмотреть все данные в ДатаФрейме шумов(noise_data), и вместо значений NaN установить
        # значение максимального шума на этой частоте с других направлений
        for angle in noise_data:
            for frequency in noise_data[angle].index.values:
                if np.isnan(noise_data[angle][frequency]):
                    noise_data[angle][frequency] = noise_data.loc[frequency].max()

        # Пересмотреть все данные в ДатаФрейме сигналов(signal_data), и вместо значений NaN установить
        # значение 0 или максимального шума на этой частоте с других направлений уменьшенное на 10 дБ (смотря, что ниже)
        for angle in signal_data:
            for frequency in signal_data[angle].index.values:
                if np.isnan(signal_data[angle][frequency]):
                    signal_data[angle][frequency] = min(0, noise_data.loc[frequency].max() - 10)

        data_s = signal_data.sort_index().T.sort_index()
        data_n = noise_data.sort_index().T.sort_index()

        # Добавить в конец ДатаФрейма данные начальной точки, чтобы график замкнулся
        self.data = pd.concat([data_s, data_s[:0]])
        self.noise = pd.concat([data_n, data_n[:0]])

        return self.data


class RadarLevelsPlotter(BaseRadarPlotter):
    """Класс построителя круговых диаграмм по подготовленным данным об Уровнях сигналов в RadarData"""

    def __init__(self, radar_data: RadarDataLevels, radar_data2: RadarDataLevels = None, y_max: int = None,
                 col_count: int = 4):
        """
        Подготавливает графики с Уровнями сигналов к отображению

        :param radar_data: данные об уровнях сигналов по углам первого измерения
        :param radar_data2: данные об уровнях сигналов по углам второго измерения для отображения на графиках
        с первыми данными
        :param y_max: Предел шкалы уровней сигналов
        :param col_count: Количество колонок с графиками
        """
        self.col_count = col_count
        BaseRadarPlotter.__init__(self, radar_data, radar_data2, y_max)


    # todo: объединить методы создания списка частот тут и в RadarDataLevels
    def _set_frequencies_list(self, data1: pd.DataFrame, data2: pd.DataFrame = None) -> pd.Series:
        """
        Формирует общий список частот из всех выборок
        :param data1: Первая выборка
        :param data2: Вторая выборка
        :return: Список частот
        """
        frequency_set = set()

        # Каджую частоту из выборок добавить в set, который обеспечивает уникальность частот
        for freq in data1.columns.values:
            frequency_set.add(freq)
        if data2 is not None:
            for freq in data2.columns.values:
                frequency_set.add(freq)

        # Сортируем и устанавливаем set, преобразованный в list, в список частот
        frequency_list = pd.Series(sorted(frequency_set))
        return frequency_list

    def _make_plot(self):
        """Из данных об Уровнях сигнала на различных угла подготавливает круговые диаграммы для каждой частоты"""

        # Список частот сохранить в self.frequencies
        # Получить общий список частот двух выборок, если data2 не равна None
        if self.rdata2 is None:
            self.frequency_list = self._set_frequencies_list(self.rdata.data)
        else:
            self.frequency_list = self._set_frequencies_list(self.rdata.data, self.rdata2.data)

        # Список углов, на которых проводились измерения надо сохранить в self.angels,
        self.angels = self.rdata.data.index.values
        # если углы первой и второй выборки отличаются, то надо выкинуть ошибку  todo

        # Рассчет количества графиков по вертикали и горизонтали
        self.row_count = math.ceil(len(self.frequency_list) / self.col_count)

        # Размер холста
        plt.figure(layout='constrained', figsize=(self.col_count * 2.5, self.row_count * 3))

        # Получение максимального значения сетки для шкалы уровней
        if self.y_max is None:
            if self.rdata2 is None:
                self._set_y_max(self.rdata.data)
            else:
                self._set_y_max(self.rdata.data, self.rdata2.data)

        # Для каждой частоты данных (todo: из спискачастот) подготовить график
        # for col_name, data in self.rdata.data.items():
        for frequency in self.frequency_list:
            axes = plt.subplot(self.row_count, self.col_count,
                               pd.Index(self.frequency_list).get_loc(frequency) + 1, projection='polar')

            # Настройка шкалы уровней текущего графика
            plt.ylim((0, self.y_max))

            # Общие настройки графиков
            min_color_ratio = 10
            min_width_ratio = -10

            if frequency in self.rdata.data.columns.values:
                data = self.rdata.data[frequency]

                # Настройка цвет и ширины бара
                color_ratio_s = (data - min_color_ratio) / (self.y_max - min_color_ratio)
                color_ratio_n = (self.rdata.noise[frequency] - min_color_ratio) / (self.y_max - min_color_ratio)
                colors_s = plt.cm.jet(color_ratio_s)
                colors_n = plt.cm.jet(color_ratio_n)

                # todo: навести порядок на рефайкторинге
                width_ratio = (data - min_width_ratio) / (self.y_max - min_width_ratio)
                if self.rdata2 is not None:
                    signal_max = max(self.rdata.data.max().max(), self.rdata2.data.max().max())
                    width_ratio = (data - min_width_ratio) / (signal_max - min_width_ratio)
                width = (2 * np.pi / data.shape[0]) * width_ratio

                # Построение графика шума
                axes.bar(data.index.values, self.rdata.noise[frequency], width=0.81, edgecolor='dimgray', color=colors_n,
                         linewidth=0.6, zorder=1)
                # Если есть только одна выборка, то бары сигнала во всю ширину сектора, иначе вполовину, сместить
                # и покрасить ребра в различимые цвета todo
                offset1 = 0
                width_offset_ratio = 1
                Line = namedtuple('Properties', 'color style width')
                self.line1 = Line('gray', '-', 0.4)
                if self.rdata2 is not None:
                    width_offset_ratio = -0.5
                    offset1 = (width * width_offset_ratio) / 2
                    Line = namedtuple('Properties', 'color style width')    # todo: убрать перечисление Line из сделать класс
                    self.line1 = Line('mediumblue', '--', 1)

                # Построить график сигнала
                axes.bar(data.index.values+offset1, data,
                         width=width*width_offset_ratio,
                         edgecolor=self.line1.color, color=colors_s,
                         linewidth=self.line1.width, zorder=4)

            # Если есть вторая выборка, построить дня нее график todo
            if self.rdata2 is not None:
                if frequency in self.rdata2.data.columns.values:
                    data = self.rdata2.data[frequency]

                    # Настройка цвет и ширины бара
                    color_ratio_s = (data - min_color_ratio) / (self.y_max - min_color_ratio)
                    color_ratio_n = (self.rdata2.noise[frequency] - min_color_ratio) / (self.y_max - min_color_ratio)
                    colors_s = plt.cm.jet(color_ratio_s)
                    colors_n = plt.cm.jet(color_ratio_n)

                    # todo: навести порядок на рефайкторинге
                    signal_max = max(self.rdata.data.max().max(), self.rdata2.data.max().max())
                    width_ratio = (data - min_width_ratio) / (signal_max - min_width_ratio)
                    width = (2 * np.pi / data.shape[0]) * width_ratio

                    # Построение графика шума
                    if frequency not in self.rdata.data.columns.values:
                        axes.bar(data.index.values, self.rdata2.noise[frequency], width=0.81, edgecolor='dimgray', color=colors_n,
                                 linewidth=0.6, zorder=1)

                    # Если есть только одна выборка, то бары сигнала во всю ширину сектора, иначе вполовину, сместить
                    # и покрасить ребра в различимые цвета todo
                    offset1 = 0
                    width_offset_ratio = 1
                    if self.rdata2 is not None:
                        width_offset_ratio = 0.5
                        offset1 = (width * width_offset_ratio) / 2
                        Line = namedtuple('Properties', 'color style width')    # todo: убрать перечисление Line из сделать класс
                        self.line1 = Line('firebrick', '--', 1)

                    # Построить график сигнала
                    axes.bar(data.index.values+offset1, data,
                             width=width*width_offset_ratio,
                             edgecolor=self.line1.color, color=colors_s,
                             linewidth=self.line1.width, zorder=4)



            # Настройка сетки графика
            axes.tick_params(axis='both', which='major', labelsize=8)
            axes.set_yticks(np.arange(0, self.y_max, 10))
            axes.set_yticks(np.arange(0, self.y_max, 2), minor=True)
            axes.grid(which='minor', color='lightgray', linewidth=0.3, alpha=0.3)
            axes.grid(which='major', linewidth=0.4, alpha=0.9)

            # Название текущего графика
            plt.title(f"{data.name} МГц", loc='center')

    def _set_y_max(self, df: pd.DataFrame, df2: pd.DataFrame = None) -> None:
        """
        Установка максимального предела шкалы графика уровней (self.y_max) кратным 10 исходя из максимальных уровней
        данных в выборке(выборках)
        :param df: первая выборка данных
        :param df2: вторая выборка данных
        """
        y_max = df.max().max()
        if df2 is not None:
            y_max2 = df2.max().max()
            y_max = max(y_max, y_max2)
        self.y_max = math.ceil(y_max / 10) * 10
