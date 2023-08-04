import unittest
import pathlib


from radar_chart.radarplot.levels_plot import RadarDataLevels, RadarLevelsPlotter


class TestLevels(unittest.TestCase):

    def test_smoke_radar_data(self):
        """Тестируем, что данные вообще обрабатываются и объект класса создается"""

        path = pathlib.Path(r'data/DataSet 1/DVI ВП').resolve()
        radar_data = RadarDataLevels(str(path))
        self.assertIsNotNone(radar_data)

    def test_smoke_radar_plotter(self):
        """Тестируем, что плоттер для вывода графиков создаётся"""

        import matplotlib
        matplotlib.get_backend()
        matplotlib.use('TkAgg')

        path = pathlib.Path(r'data/DataSet 1/DVI ВП').resolve()
        radar_data = RadarDataLevels(str(path))
        plotter = RadarLevelsPlotter(radar_data)
        self.assertIsNotNone(plotter)
