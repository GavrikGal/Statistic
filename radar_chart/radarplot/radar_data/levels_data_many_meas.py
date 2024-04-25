import os

import numpy as np
import pandas as pd
from typing import List

from .base_many_meas_data import BaseManyMeasData
from ..utils import make_unique_frequency_list


MIN_VALUE = 0


class RadarDataLevelsManyMeas(BaseManyMeasData):
    """Класс данных для круговых диаграмм уровней излучений, измеренных в различных
    направлениях от изделия для множества измерений"""

    def __init__(self, dir_path: str):
        """
        Подготавливает данные об уровнях излучений (на всех углах измерений) из папки dir_path
        для отображения их на круговых диаграммах
        :param dir_path: путь к папке со списком файлов данных
        """
        BaseManyMeasData.__init__(self, dir_path)

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

        # # Инициировать DataFrame
        raw_data = pd.DataFrame(columns=['meas_name', 'interface', 'polarisation', 'angle', 'freq', 'signal', 'noise'])

        # Перебрать все файлы и составить датафреймы сигналов и шумов
        for file in self.files:
            # получить величину угла из названия файла
            meas_name = self._get_meas_name(file)
            interface = self._get_interface(file)
            polarisation = self._get_polarisation(file)
            filename = self._get_filename(file)
            angle = self.get_angle_from_filename(filename)

            # прочитать данные частоты, уровня сигнала и шума из файла
            # частоты установить в качестве индексов DataFrame
            file_dataframe = pd.read_csv(file, sep='\t', encoding='cp1251',
                                         usecols=[1, 2, 3], skiprows=2, names=['freq', 'signal', 'noise'])
            file_dataframe['meas_name'] = meas_name
            file_dataframe['interface'] = interface
            file_dataframe['polarisation'] = polarisation
            file_dataframe['angle'] = angle
            file_dataframe['freq'] = file_dataframe['freq'].round(1)
            raw_data = pd.concat([raw_data, file_dataframe], ignore_index=True)
        print("-" * 28, 'raw_data', "-" * 28)
        print(f'{raw_data}')
        print("-"*60)

        grouped = raw_data.groupby(['meas_name', 'angle', 'freq'],
                                   as_index=False).max()[['meas_name', 'angle', 'freq', 'signal', 'noise']]

        df_after_grouped = pd.DataFrame(grouped)

        signal_data = df_after_grouped.groupby(['angle', 'freq'])['signal'].mean().round(1).unstack(level='angle')

        noise_data = df_after_grouped.groupby(['angle', 'freq'])['noise'].mean().round(1).unstack(level='angle')

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
