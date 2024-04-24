import abc
import pathlib
from typing import List

from .base import BaseRadarData


class BaseManyMeasData(BaseRadarData, abc.ABC):
    """ Базовый класс для данных к круговым диаграммам, читаемым из многих файлов """

    def __init__(self, dir_path: str):
        """
        Перенаправляет создание объекта базовому классу

        :param dir_path: путь к начальной папке с данными
        """
        BaseRadarData.__init__(self, dir_path)

    def read_filenames(self) -> List[pathlib.Path]:
        """
        Прочитать список файлов из заданной папки

        :return: список текстовых файлов
        """
        meas_dir_list = [dirname for dirname in self.dir.iterdir() if dirname.is_dir()]

        file_list = []
        for meas_dir in meas_dir_list:
            for polarisation in meas_dir.iterdir():
                file_list.extend([meas_file for meas_file in polarisation.iterdir()
                                  if meas_file.is_file() and meas_file.name.endswith('.txt')])

        return file_list

    def _get_meas_name(self, file: pathlib.Path) -> str:
        """Из пути к файлу измерений получить имя измерения"""
        return file.relative_to(self.dir).parts[0]

    def _get_interface(self, file: pathlib.Path) -> str:
        """Из пути к файлу измерений получить название интерфейса"""
        return file.relative_to(self.dir).parts[1].split(" ")[0]

    def _get_polarisation(self, file: pathlib.Path) -> str:
        """Из пути к файлу измерений получить поляризацию"""
        return file.relative_to(self.dir).parts[1].split(" ")[1]

    def _get_filename(self, file: pathlib.Path) -> str:
        """Из пути к файлу измерений получить имя файла"""
        return file.name
