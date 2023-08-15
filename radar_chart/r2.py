import matplotlib

from radarplot.r2_plot import RadarDataR2, RadarR2Plotter


DIR_NAME = r'd:\WorkSpace\Python\pythonProject\Statistic\data\ВМЦ-61.2ЖК\1903103\Доработка 4 (Стекло НВИТ...317)\DVI max'
DIR2_NAME = None

# Если надо отрубить второй набор данных, то комментить следующую строчку
DIR2_NAME = r'd:\WorkSpace\Python\pythonProject\Statistic\data\ВМЦ-61.2ЖК\1903103\Доработка 5 (Уплотнители в задней части корпуса + дораб LVDS)\DVI max'

if __name__ == '__main__':
    matplotlib.get_backend()
    matplotlib.use('QtAgg')

    data1 = RadarDataR2(DIR_NAME)
    if DIR2_NAME is None:
        data2 = None
    else:
        data2 = RadarDataR2(DIR2_NAME)
        data_list = [data1, data2]

    plotter = RadarR2Plotter(data1, data2, radar_data_list=data_list, max_y_tick=17)
    # plotter.show()
    plotter.save(DIR2_NAME + ' [Сравнение R2].png')
