import matplotlib

from radarplot.radar_data import RadarDataR2ManyMeas
from radarplot.plotter import RadarR2Plotter


DIR_NAME = r'd:\WorkSpace\Python\pythonProject\Statistic\data\ЭВМ БК-ТЗ-4К\9. VGA [кабель - НВИТ, нагрузка - БК-ТЗ-А1] (все частоты + фон)'
DIR2_NAME = None

# Если надо отрубить второй набор данных, то комментить следующую строчку
# DIR2_NAME = r'd:\WorkSpace\Python\pythonProject\Statistic\data\ВМЦ-61.2ЖК\Монитор без краски\Ток прошивки\LVDS max'

if __name__ == '__main__':
    matplotlib.get_backend()
    matplotlib.use('QtAgg')

    data1 = RadarDataR2ManyMeas(DIR_NAME)
    if DIR2_NAME is None:
        data_list = [data1]
        output_file_name = DIR_NAME + ' [График R2].png'
    else:
        data2 = RadarDataR2ManyMeas(DIR2_NAME)
        data_list = [data1, data2]
        output_file_name = DIR2_NAME + ' [Сравнение R2].png'

    plotter = RadarR2Plotter(data_list, max_y_tick=18)
    # plotter = RadarR2Plotter(data_list, max_y_tick=17)
    # plotter.show()
    plotter.save(output_file_name)
