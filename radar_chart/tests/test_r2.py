import unittest
import pathlib


from radar_chart.radarplot.radar_data import RadarDataR2
from radar_chart.radarplot.plotter import RadarR2Plotter


class TestR2(unittest.TestCase):

    def test_smoke_radar_data(self):
        """Тестируем, что данные вообще обрабатываются и объект класса создается"""

        path = pathlib.Path(r'radar_chart/tests/data/DataSet 1/DVI ВП').resolve()
        radar_data = RadarDataR2(str(path))
        self.assertIsNotNone(radar_data)

    def test_smoke_radar_plotter(self):
        """Тестируем, что плоттер для вывода графиков создаётся"""

        import matplotlib
        matplotlib.get_backend()

        path = pathlib.Path(r'radar_chart/tests/data/DataSet 1/DVI ВП').resolve()
        radar_data = RadarDataR2(str(path))
        plotter = RadarR2Plotter([radar_data])
        self.assertIsNotNone(plotter)
