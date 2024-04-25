import unittest
import pathlib


from radar_chart.radarplot.plotter import RadarLevelsPlotter
from radar_chart.radarplot.radar_data import RadarDataLevelsManyMeas


class TestLevelsManyData(unittest.TestCase):

    def test_smoke_radar_data(self):
        """Тестируем, что данные вообще обрабатываются и объект класса создается"""

        path = pathlib.Path(r'radar_chart/tests/data/DataSet 3/1. DVI [кабель - доработанный, нагрузка - монитор Asus]').resolve()
        radar_data = RadarDataLevelsManyMeas(str(path))
        self.assertIsNotNone(radar_data)

    def test_smoke_radar_plotter(self):
        """Тестируем, что плоттер для вывода графиков создаётся"""

        import matplotlib
        matplotlib.get_backend()
        # matplotlib.use('TkAgg')

        path = pathlib.Path(r'radar_chart/tests/data/DataSet 3/1. DVI [кабель - доработанный, нагрузка - монитор Asus]').resolve()
        radar_data = RadarDataLevelsManyMeas(str(path))
        plotter = RadarLevelsPlotter([radar_data])
        self.assertIsNotNone(plotter)

    def test_radar_many_data_level_plotter_makes_file_with_plot(self):
        """Тестируем, что создается файл графика Уровней"""
        import matplotlib
        matplotlib.get_backend()
        matplotlib.use('QtAgg')
        path = pathlib.Path(
            r'radar_chart/tests/data/DataSet 3/1. DVI [кабель - доработанный, нагрузка - монитор Asus]').resolve()
        output_name = str(path) + '_test_plot.png'
        radar_data = RadarDataLevelsManyMeas(str(path))
        plotter = RadarLevelsPlotter([radar_data])
        plotter.save(output_name)
        self.assertTrue(pathlib.Path(output_name).exists())

        # Удаление созданного файла
        output_file = pathlib.Path(output_name)
        output_file.unlink()
