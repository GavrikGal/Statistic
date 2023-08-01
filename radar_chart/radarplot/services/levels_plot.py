import math
import os

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from typing import List

from .base import BaseRadarData, BaseRadarPlotter


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
                                      skiprows=2).values
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
        frequencies = self._read_frequency_set()

        # Инициировать DataFrame сигналов и шумов с частотами в качестве индексов
        signal_data = pd.DataFrame(index=np.array(frequencies))
        noise_data = pd.DataFrame(index=np.array(frequencies))

        # Перебрать все файлы и вычитать есть ли в них данные на тех частотах, список которых нашли ранее
        for filename in self.files:
            # получить величину угла из названия файла
            angle = self._get_angle_from_filename(filename)

            # прочитать данные частоты, уровня сигнала и шума из файла
            # частоты установить в качестве индексов DataFrame
            file_dataframe = pd.read_csv(os.path.join(self.dir, filename), sep='\t', encoding='cp1251',
                                         usecols=[1, 2, 3], skiprows=1, index_col=0)

            # заполнить ДатаФреймы сигналов и шумов
            for frequency in file_dataframe.index.values:
                signal_data.at[frequency, angle] = file_dataframe.loc[frequency][0]
                noise_data.at[frequency, angle] = file_dataframe.loc[frequency][1]

        # Пересмотреть все данные в ДатаФрейме сигналов(signal_data_frame), и вместо значений NaN установить
        # значение минимального шума на этой частоте из ДатаФрейма шумов(noise_data_frame)
        for angle in signal_data:
            for frequency in signal_data[angle].index.values:
                if np.isnan(signal_data[angle][frequency]):
                    signal_data[angle][frequency] = noise_data.loc[frequency].max()

        # Сортируем и транспорируем полученные данные
        data = signal_data.sort_index().T.sort_index()

        # Добавить в конец ДатаФрейма данные начальной точки, чтобы график замкнулся
        data = pd.concat([data, data[:0]])

        return data


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

    def _make_plot(self):
        """Из данных об Уровнях сигнала на различных угла подготавливает круговые диаграммы для каждой частоты"""

        # Рассчет количества графиков по вертикали и горизонтали
        self.row_count = math.ceil(self.rdata.data.shape[1] / self.col_count)

        # Размер холста
        plt.figure(layout='constrained', figsize=(self.col_count * 2.5, self.row_count * 3))

        # Получение максимального значения сетки для шкалы уровней
        if self.y_max is None:
            self._set_y_max(self.rdata.data)

        # Для каждой частоты данных подготовить график
        for col_name, data in self.rdata.data.items():

            axes = plt.subplot(self.row_count, self.col_count,
                               self.rdata.data.columns.get_loc(col_name) + 1, projection='polar')

            # Настройка шкалы уровней текущего графика
            plt.ylim((0, self.y_max))

            # Построение линии на графике
            min_color_ratio = 10
            color_ratio = (data - min_color_ratio) / (self.rdata.data.max().max() - min_color_ratio)
            colors = plt.cm.jet(color_ratio)
            min_width_ratio = -10
            width_ratio = (data - min_width_ratio) / (self.rdata.data.max().max() - min_width_ratio)
            width = (2 * np.pi / data.shape[0]) * width_ratio
            axes.bar(data.index.values, data, width=width, edgecolor='gray', color=colors, linewidth=0.2, zorder=3)
            # plt.plot(data, color=self.line1.color, linewidth=self.line1.width)

            # Настройка сетки графика
            axes.tick_params(axis='both', which='major', labelsize=8)
            axes.set_yticks(np.arange(0, self.y_max, 10))
            axes.set_yticks(np.arange(0, self.y_max, 2), minor=True)
            axes.grid(which='minor', color='lightgray', linewidth=0.3, alpha=0.3)
            axes.grid(which='major', linewidth=0.4, alpha=0.9)

            # Название текущего графика
            plt.title(f"Frequency - {data.name} MHz ", loc='center')

    def _set_y_max(self, df: pd.DataFrame) -> None:
        y_max = df.max().max()
        self.y_max = math.ceil(y_max / 10) * 10
