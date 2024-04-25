import unittest
import pathlib


from radar_chart.radarplot.radar_data import RadarDataR2ManyMeas
from radar_chart.radarplot.plotter import RadarR2Plotter


class TestR2ManyData(unittest.TestCase):

    def test_smoke_radar_many_data(self):
        """Тестируем, что данные вообще обрабатываются и объект класса создается"""

        path = pathlib.Path(r'radar_chart/tests/data/DataSet 3/1. DVI [кабель - доработанный, нагрузка - монитор Asus]').resolve()
        radar_data = RadarDataR2ManyMeas(str(path))
        self.assertIsNotNone(radar_data)

    def test_smoke_radar_many_data_plotter(self):
        """Тестируем, что плоттер для вывода графиков создаётся"""

        import matplotlib
        matplotlib.get_backend()
        # matplotlib.use('TkAgg')

        path = pathlib.Path(r'radar_chart/tests/data/DataSet 3/1. DVI [кабель - доработанный, нагрузка - монитор Asus]').resolve()
        radar_data = RadarDataR2ManyMeas(str(path))
        plotter = RadarR2Plotter([radar_data])
        self.assertIsNotNone(plotter)

    def test_radar_many_data_R2_plotter_makes_file_with_plot(self):
        """Тестируем, что создается файл графика R2"""
        import matplotlib
        matplotlib.get_backend()
        # matplotlib.use('QtAgg')
        path = pathlib.Path(
            r'radar_chart/tests/data/DataSet 3/1. DVI [кабель - доработанный, нагрузка - монитор Asus]').resolve()
        output_name = str(path) + '_test_plot.png'
        radar_data = RadarDataR2ManyMeas(str(path))
        plotter = RadarR2Plotter([radar_data])
        plotter.save(output_name)
        self.assertTrue(pathlib.Path(output_name).exists())

        # Удаление созданного файла
        output_file = pathlib.Path(output_name)
        output_file.unlink()
