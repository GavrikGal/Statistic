import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pathlib
import re
from typing import List, Tuple


class RadarData(object):
    """Класс данных для круговых диаграмм зон R2 по углам"""

    def __init__(self, dir_path: str):
        """
        Подготавливает данные о зонах R2 (на всех углах измерения) для отображения их на круговых диаграммах

        :param dir_path: путь к папке со списком файлов данных
        """
        self.dir: pathlib.Path = pathlib.Path(dir_path)
        self.files: List[str] = self._read_filenames()
        self.data: pd.Series = self._make_data()

    def _read_filenames(self) -> List[str]:
        """
        Прочитать список файлов из заданной папки

        :return: список текстовых файлов
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


class RadarPlotter(object):
    """Класс построителя круговых диаграмм по подготовленным данным о зонах R2 в RadarData"""

    def __init__(self, radar_data: RadarData, radar_data2: RadarData = None):
        """
        Подготавливает графики с зонами R2 к отображению

        :param radar_data: данные о R2 по углам
        :param radar_data2: второй набор данных о R2 для сравнения с первым
        """
        self.data: pd.Series = radar_data.data
        self.data2: pd.Series = radar_data.data
        self.plt = plt
        self.plt.figure(layout='constrained', figsize=(5, 6))   # Размер холста

        # Добавить в конец ДатаСерии данные начальной точки, чтобы график замкнулся
        print(self.data)
        first = self.data.loc[0]
        print(type(first))
        # data = pd.concat([self.data, self.data[0]])
        # print(data)

        # Получение списка углов из значений индексов ДатаФрейма
        angles = self.data.index.values
        self.plt.plot(np.deg2rad(angles), self.data, color='r', linewidth=1.8)
