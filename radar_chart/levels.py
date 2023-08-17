import matplotlib

from radarplot.radar_data import RadarDataLevels
from radarplot.plotter import RadarLevelsPlotter


DIR_NAME = r'd:\WorkSpace\Python\pythonProject\Statistic\data\ВМЦ-61.2ЖК\1903103\Доработка 4 (Стекло НВИТ...317)\LVDS ГП'
DIR2_NAME = None

# Если надо отрубить второй набор данных, то комментить следующую строчку
DIR2_NAME = r'd:\WorkSpace\Python\pythonProject\Statistic\data\ВМЦ-61.2ЖК\1903103\Доработка 5 (Уплотнители в задней части корпуса + дораб LVDS)\LVDS ГП'


if __name__ == '__main__':
    matplotlib.get_backend()
    matplotlib.use('QtAgg')

    data_list = None

    data1 = RadarDataLevels(DIR_NAME)
    if DIR2_NAME is None:
        data2 = None
    else:
        data2 = RadarDataLevels(DIR2_NAME)
        data_list = [data1, data2]

    plotter = RadarLevelsPlotter(data1, data2, radar_data_list=data_list, max_y_tick=50)
    # plotter.show()
    if DIR2_NAME is None:
        plotter.save(DIR_NAME + ' [Уровни].png')
    else:
        plotter.save(DIR2_NAME + ' [Сравнение уровней].png')
