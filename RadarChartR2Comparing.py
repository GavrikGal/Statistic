import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import os
import pathlib
import math
import re
from typing import List, Tuple


DIR_NAME = r'd:\WorkSpace\Python\pythonProject\Statistic\data\ВМЦ-61.2ЖК\1903103\Доработка 2 (Поменяли стекло)\LVDS ВП'

# TODO: Добавить возможность расчета из другой папки со сравнением на соответствующих графиках
DIR2_NAME =r'd:\WorkSpace\Python\pythonProject\Statistic\data\ВМЦ-61.2ЖК\1903103\Доработка 3 (Матрица обклеена лентой)\LVDS ВП'


class RadarData(object):
    def __init__(self, dir_path: str):
        self.dir: pathlib.Path = pathlib.Path(dir_path)
        self.files: List[str] = self._read_filenames()      # Прочитать список файлов из рабочей папки
        self.data: pd.Series = self._make_data()            # Собрать данные по R2 из списка файлов

    def _read_filenames(self) -> List[str]:
        """
        Прочитать список файлов из заданной папки
        :return: список файлов
        """
        file_list = [file.name for file in self.dir.iterdir() if file.is_file() and file.name.endswith('.txt')]
        return file_list

    def _make_data(self) -> pd.Series:
        """
        Читает имя каждого файла из списка self.files парсит в нем угол, на котором проводились измерения, и
        результат рассчитанной зоны R2. Из этих данных формирует ДатаСерию для всех положений (углов) измерений
        :return: ДатаСерия с углами, в качестве индексов, и R2, в качестве значений
        """

        angles, r2_list = [], []
        # Перебрать названия всех файлов папки и выбрать из них угол,
        # на котором проводились измерения, и радиус зоны R2
        for filename in self.files:
            angle, r2 = self._get_angle_and_r2_from_filename(filename)
            angles.append(angle)
            r2_list.append(r2)
        return pd.Series(r2_list, index=angles).sort_index()

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


if __name__ == '__main__':
    matplotlib.get_backend()
    matplotlib.use('TkAgg')

    data1 = RadarData(DIR_NAME)
    data2 = RadarData(DIR2_NAME)
