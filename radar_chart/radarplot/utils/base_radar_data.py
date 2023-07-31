import abc
import pandas as pd
import pathlib
import re
from typing import List, Union


class BaseRadarData(abc.ABC):
    """Базовый Класс данных для круговых диаграмм зон R2 по углам"""

    def __init__(self, dir_path: str):
        """
        Подготавливает данные о зонах R2 (на всех углах измерения) для отображения их на круговых диаграммах

        :param dir_path: путь к папке со списком файлов данных
        """
        self.dir: pathlib.Path = pathlib.Path(dir_path)
        self.files: List[str] = self._read_filenames()
        self.data: Union[pd.Series, pd.DataFrame] = self._make_data()

    def _read_filenames(self) -> List[str]:
        """
        Прочитать список файлов из заданной папки

        :return: список текстовых файлов
        """
        file_list = [file.name for file in self.dir.iterdir() if file.is_file() and file.name.endswith('.txt')]
        return file_list

    @abc.abstractmethod
    def _make_data(self) -> Union[pd.Series, pd.DataFrame]:
        """
        Читает имя каждого файла из списка self.files парсит в нем угол, на котором проводились измерения, и
        результат рассчитанной зоны R2. Из этих данных формирует ДатаСерию для всех положений (углов) измерений

        :return: ДатаСерия с углами, в качестве индексов, и R2, в качестве значений
        """

        # data_set = {}
        # # Перебрать названия всех файлов папки и выбрать из них угол,
        # # на котором проводились измерения, и радиус зоны R2
        # for filename in self.files:
        #     angle, r2 = self._get_angle_and_r2_from_filename(filename)
        #     data_set[np.deg2rad(angle)] = r2
        #
        # # Создать объект данных pandas и отсортировать его
        # data = pd.Series(data_set).sort_index()
        #
        # # Добавить в конец ДатаСерии данные начальной точки, чтобы график замкнулся
        # data = pd.concat([data, data[:0]])
        #
        # return data

    @staticmethod
    def _get_angle_from_filename(filename: str) -> float:
        """
        Парсит имя файла на угол, на котором проводились измерения, и результат рассчитанной зоны R2

        :param filename: имя файла
        :return: угол, R2
        """
        angle = float(re.findall(r'\((\d+)\)', filename)[0])
        return angle

    @staticmethod
    def _get_r2_from_filename(filename: str) -> float:
        """
        Парсит имя файла на угол, на котором проводились измерения, и результат рассчитанной зоны R2

        :param filename: имя файла
        :return: угол, R2
        """
        r2 = float(re.findall(r'\) (\d+)', filename)[0])
        return r2
