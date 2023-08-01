import matplotlib

from radarplot.services import RadarDataR2, RadarR2Plotter


DIR_NAME = r'd:\WorkSpace\Python\pythonProject\Statistic\data\ВМЦ-61.2ЖК\1903103\Доработка 2 (Поменяли стекло)\LVDS ГП'
DIR2_NAME = None

# Если надо отрубить второй набор данных, то комментить следующую строчку
DIR2_NAME =r'd:\WorkSpace\Python\pythonProject\Statistic\data\ВМЦ-61.2ЖК\1903103\Доработка 3 (Матрица обклеена лентой)\LVDS ГП'

if __name__ == '__main__':
    matplotlib.get_backend()
    matplotlib.use('TkAgg')

    data1 = RadarDataR2(DIR_NAME)
    if DIR2_NAME is not None:
        data2 = RadarDataR2(DIR2_NAME)
    else:
        data2 = None

    plotter = RadarR2Plotter(data1, data2, y_max=15)
    plotter.show()
    plotter.save(r'd:\WorkSpace\Python\pythonProject\Statistic\data\ВМЦ-61.2ЖК\1903103\Доработка 3 (Матрица обклеена лентой)\LVDS ГП [доработка2, доработка3]')
