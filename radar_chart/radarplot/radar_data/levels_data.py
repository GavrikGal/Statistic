import os

import numpy as np
import pandas as pd
from typing import List

from .base import BaseRadarData
from ..utils import make_unique_frequency_list


MIN_VALUE = 0


class RadarDataLevels(BaseRadarData):
    """Класс данных для круговых диаграмм уровней излучений, измеренных в различных
    направлениях от изделия"""

    def __init__(self, dir_path: str):
        """
        Подготавливает данные об уровнях излучений (на всех углах измерений) из папки dir_path
        для отображения их на круговых диаграммах
        :param dir_path: путь к папке со списком файлов данных
        """
        BaseRadarData.__init__(self, dir_path)

    def read_frequency_set(self) -> List[float]:
        """
        Получить список всех частот, на которых обнаружены сигналы, из всех файлов с данными
        :return: список частот
        """

        frequency_list = []
        # Прочитать все файлы с данными из папки self.dir и из каждого прочитать список частот
        for filename in self.files:
            frequencies = pd.read_csv(os.path.join(self.dir, filename), sep='\t', encoding='cp1251', usecols=[1],
                                      skiprows=1, index_col=0)

            # Каждый набор частот добавить в список
            frequency_list.append(frequencies)
        # Оставляем только уникальные частоты в списке
        frequency_list = make_unique_frequency_list(frequency_list)

        return sorted(frequency_list)

    def make_data(self) -> pd.DataFrame:
        """
        Читает имя каждого файла из списка self.files парсит в нем угол, на котором проводились измерения,
        и измеренный уровень сигнала. Из этих данных формирует ДатаФрейм для всех положений (углов) измерений
        и для всех частот, на которых обнаружены сигналы

        :return: ДатаСерия с углами, в качестве индексов, и уровнями сигнала, в качестве значений
        """

        # Получить список всех частот из всех файлов
        # self.frequencies = self.read_frequency_set()

        # # Инициировать DataFrame сигналов и шумов с частотами в качестве индексов
        # signal_data = pd.DataFrame(index=np.array(self.frequencies))
        # noise_data = pd.DataFrame(index=np.array(self.frequencies))

        signal_data = pd.DataFrame()
        noise_data = pd.DataFrame()

        # Перебрать все файлы и составить датафреймы сигналов и шумов
        for filename in self.files:
            # получить величину угла из названия файла
            angle = self.get_angle_from_filename(filename)

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
        # Значение шума не должно быть ниже MIN_VALUE
        for angle in noise_data:
            for frequency in noise_data[angle].index.values:
                if np.isnan(noise_data[angle][frequency]):
                    noise_data[angle][frequency] = noise_data.loc[frequency].max()
                if noise_data[angle][frequency] < MIN_VALUE:
                    noise_data[angle][frequency] = MIN_VALUE

        # Пересмотреть все данные в ДатаФрейме сигналов(signal_data), и
        # вместо значений NaN установить значение MIN_VALUE
        # Значение сигнала не должно быть ниже MIN_VALUE
        for angle in signal_data:
            for frequency in signal_data[angle].index.values:
                if np.isnan(signal_data[angle][frequency]):
                    signal_data[angle][frequency] = min(MIN_VALUE, noise_data.loc[frequency].max() - 10)
                if signal_data[angle][frequency] < MIN_VALUE:
                    signal_data[angle][frequency] = MIN_VALUE

        data_s = signal_data.sort_index().T.sort_index()
        data_n = noise_data.sort_index().T.sort_index()

        self.data = data_s
        self.noise = data_n

        return self.data
