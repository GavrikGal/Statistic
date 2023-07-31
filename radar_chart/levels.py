import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import os
import math
import re
from typing import List

from radarplot.utils.base_radar_data import BaseRadarData


DIR_NAME = r'd:\WorkSpace\Python\pythonProject\Statistic\data\ВМЦ-61.2ЖК\1903103\Доработка 2 (Поменяли стекло)\LVDS ГП'

# TODO: Добавить возможность расчета из другой папки со сравнением на соответствующих графиках
# DIR2_NAME


class RadarDataFrame(BaseRadarData):
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
        signal_data_frame = pd.DataFrame(index=np.array(frequencies))
        noise_data_frame = pd.DataFrame(index=np.array(frequencies))

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
                signal_data_frame.at[frequency, angle] = file_dataframe.loc[frequency][0]
                noise_data_frame.at[frequency, angle] = file_dataframe.loc[frequency][1]

        # Пересмотреть все данные в ДатаФрейме сигналов(signal_data_frame), и вместо значений NaN установить
        # значение минимального шума на этой частоте из ДатаФрейма шумов(noise_data_frame)
        for angle in signal_data_frame:
            for frequency in signal_data_frame[angle].index.values:
                if np.isnan(signal_data_frame[angle][frequency]):
                    signal_data_frame[angle][frequency] = noise_data_frame.loc[frequency].max()

        # Сортируем и транспорируем полученные данные
        signal_transpose_data_frame = signal_data_frame.sort_index().T
        sorted_signal_transpose_data_frame = signal_transpose_data_frame.sort_index()

        return sorted_signal_transpose_data_frame


# def get_angle_from_filename(filename):
#     angle = re.findall(r'\((\d+)\)', filename)[0]
#     return int(angle)


# # TODO: Рефакторинг, нахер надо постоянно гонять имя файла и папки, надо сделать для этого класс походу
# def read_frequency_set(dir_name: str, file_list: List[str]) -> List[float]:
#     frequency_set = set()
#     for filename in file_list:
#         frequencies = pd.read_csv(os.path.join(dir_name, filename), sep='\t', encoding='cp1251', usecols=[1],
#                                   skiprows=2).values
#         for freq in frequencies:
#             frequency_set.add(freq[0])
#     frequency_list = list(sorted(frequency_set))
#     return frequency_list


# def read_data_frame(dir_name: str) -> pd.DataFrame:
#     """ Чтение данных из всех файлов каталога """
#     file_list = os.listdir(dir_name)
#
#     # Получить список всех частот из всех файлов
#     frequencies = read_frequency_set(dir_name, file_list)
#
#     # Инициировать DataFrame сигналов и шумов с частотами в качестве индексов
#     signal_data_frame = pd.DataFrame(index=np.array(frequencies))
#     noise_data_frame = pd.DataFrame(index=np.array(frequencies))
#
#     # Перебрать все файлы и вычитать есть ли в них данные на тех частотах, список которых нашли ранее
#     for filename in file_list:
#         # получить величину угла из названия файла
#         angle = get_angle_from_filename(filename)
#
#         # прочитать данные частоты, уровня сигнала и шума из файла
#         # частоты установить в качестве индексов DataFrame
#         file_dataframe = pd.read_csv(os.path.join(dir_name, filename), sep='\t', encoding='cp1251', usecols=[1, 2, 3],
#                                      skiprows=1, index_col=0)
#
#         # заполнить ДатаФреймы сигналов и шумов
#         for frequency in file_dataframe.index.values:
#             signal_data_frame.at[frequency, angle] = file_dataframe.loc[frequency][0]
#             noise_data_frame.at[frequency, angle] = file_dataframe.loc[frequency][1]
#
#     # Пересмотреть все данные в ДатаФрейме сигналов(signal_data_frame), и вместо значений NaN установить
#     # значение минимального шума на этой частоте из ДатаФрейма шумов(noise_data_frame)
#     for angle in signal_data_frame:
#         for frequency in signal_data_frame[angle].index.values:
#             if np.isnan(signal_data_frame[angle][frequency]):
#                 signal_data_frame[angle][frequency] = noise_data_frame.loc[frequency].max()
#
#     # Сортируем и транспорируем полученные данные
#     signal_transpose_data_frame = signal_data_frame.sort_index().T
#     sorted_signal_transpose_data_frame = signal_transpose_data_frame.sort_index()
#
#     return sorted_signal_transpose_data_frame


def get_max_y_lim(df: pd.DataFrame) -> int:
    max_y_value = df.max().max()
    return math.ceil(max_y_value / 10) * 10


def make_plot(df: pd.DataFrame) -> None:
    """Вывод данных на график"""

    # Рассчет количества графиков по вертикали и горизонтали
    fig_cols = 4
    fig_rows = math.ceil(df.shape[1] / fig_cols)

    # Размер холста
    plt.figure(layout='constrained', figsize=(12, 14))

    # Получение максимального значения сетки для шкалы уровней
    max_y_lim = get_max_y_lim(df)

    for col_name, data in df.items():
        # Новый график в соответствующей позиции
        axes = plt.subplot(fig_rows, fig_cols, df.columns.get_loc(col_name) + 1, projection='polar')

        # Получение списка углов из значений индексов ДатаФрейма
        angles = data.index.values

        # Настройка шкалы уровней текущего графика
        plt.ylim((0, max_y_lim))

        # Непосредственное создание линий на графике
        plt.plot(np.deg2rad(angles), data, color='r', linewidth=1.8)
        plt.plot((np.deg2rad(angles[-1]), np.deg2rad(angles[0])),
                 (data[angles[-1]], data[angles[0]]), color='r', linewidth=1.8)

        # Настройка сетки графика
        axes.tick_params(axis='both', which='major', labelsize=10)
        axes.set_yticks(np.arange(0, max_y_lim, 10))
        axes.set_yticks(np.arange(0, max_y_lim, 5), minor=True)
        axes.grid(which='minor', alpha=0.3)
        axes.grid(which='major', alpha=0.9)

        # Название текущего графика
        plt.title(f"Frequency - {data.name} MHz ", loc='center')


if __name__ == '__main__':
    matplotlib.get_backend()
    matplotlib.use('TkAgg')

    df_new = RadarDataFrame(DIR_NAME)

    make_plot(df_new.data)

    plt.savefig(DIR_NAME + '_plot.png', dpi=400)
    plt.show()
