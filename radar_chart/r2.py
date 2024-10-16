import matplotlib

from radarplot.radar_data import RadarDataR2
from radarplot.plotter import RadarR2Plotter


DIR_NAME = r'd:\WorkSpace\Python\pythonProject\Statistic\data\ВМЦ-61ЖК\Оценочные (периодика со склада)\VGA ВП'
DIR2_NAME = None

# Если надо отрубить второй набор данных, то комментить следующую строчку
DIR2_NAME = r'd:\WorkSpace\Python\pythonProject\Statistic\data\ВМЦ-61ЖК\Оценочные (периодика со склада)\VGA ГП'

if __name__ == '__main__':
    matplotlib.get_backend()
    matplotlib.use('QtAgg')

    data1 = RadarDataR2(DIR_NAME)
    if DIR2_NAME is None:
        data_list = [data1]
        output_file_name = DIR_NAME + ' [График R2].png'
    else:
        data2 = RadarDataR2(DIR2_NAME)
        data_list = [data1, data2]
        output_file_name = DIR2_NAME + ' [Сравнение R2].png'
        output_file_name = DIR2_NAME + ' [ВП + ГП].png'

    plotter = RadarR2Plotter(data_list, max_y_tick=23)
    # plotter.show()
    plotter.save(output_file_name)
