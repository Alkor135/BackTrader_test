import datetime
import backtrader as bt


class TestStrategy(bt.Strategy):
    """ Простейшая система без торговли. При приходе нового бара отображает его цены и объем"""
    def log(self, txt, dt=None):
        """ Вывод строки с датой на консоль """
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()}, {txt}')

    def __init__(self):
        """ Инициализация торговой системы """
        self.increment_is_completed = False  # True - приращение в этом месяце выполнено
        self.data_open = self.datas[0].open
        self.data_high = self.datas[0].high
        self.data_low = self.datas[0].low
        self.data_close = self.datas[0].close
        self.data_volume = self.datas[0].volume

    def next(self):
        """ Приход нового бара """
        dt_1 = self.datas[0].datetime.datetime(-1)  # Дата время предыдущего бара
        # Если месяц предыдущего бара не равен месяцу текущего бара
        if datetime.datetime.timetuple(dt_1)[1] != datetime.datetime.timetuple(self.datetime.datetime())[1]:
            self.increment_is_completed = False

        if not self.increment_is_completed and increment_date <= datetime.datetime.timetuple(self.datetime.datetime())[2]:
            cerebro.broker.setcash(cerebro.broker.getvalue() + increment)
            self.increment_is_completed = True

        print(f'\n{datetime.datetime.timetuple(dt_1)[1]=}, {datetime.datetime.timetuple(self.datetime.datetime())[1]=}')
        print(f'{increment_date}, {datetime.datetime.timetuple(self.datetime.datetime())[2]=}')
        print('Текущее значение: %.2f' % cerebro.broker.getvalue())



        # self.log(f'{self.data_open[0]}, {self.data_high[0]}, {self.data_low[0]}, {self.data_close[0]}, {self.data_volume[0]}')
        # self.log(f'{self.datas[0].open[0]}')
        # self.log(f'{self.data_open}, {self.data_high}, {self.data_low}, {self.data_close}, {self.data_volume}')
        # print(self.date[0].isoformat())
        # print(self.datetime.date())  # Дата текущего бара
        # dt_1 = self.datas[-1].datetime.datetime(-1)
        # print(f'{dt_1=}')  # Дата текущего бара
        # print(datetime.datetime.timetuple(dt_1)[0])
        # print(self.datetime.date()[-1])  # Дата текущего бара
        # print(datetime.datetime.timetuple(self.datetime.datetime()))  # Тьюпл
        # print(datetime.datetime.timetuple(self.datetime.datetime())[0])  # Год
        # print(datetime.datetime.timetuple(self.datetime.datetime())[1])  # Месяц
        # print(datetime.datetime.timetuple(self.datetime.datetime())[2])  # День
        # print(type(self.datetime.date()))  # Тип
        # cerebro.broker.setcash(cerebro.broker.getvalue() + 100.00)


if __name__ == '__main__':
    increment = 10000.00  # Ежемесячное приращение
    increment_date = 15  # Дата приращения

    cerebro = bt.Cerebro()  # Инициализируем движок BackTrader
    cerebro.addstrategy(TestStrategy)  # Привязываем торговую систему

    # Create a Data Feed
    data = bt.feeds.GenericCSVData(
        dataname='data/FXIT_130101_220101.txt',
        datetime=0,
        time=1,  # поле времени присутствует и замаркеровано 1
        open=2,
        high=3,
        low=4,
        close=5,
        volume=6,
        openinterest=-1,  # поле открытого интереса отсутствует
        separator=';',
        dtformat='%Y%m%d',
        tmformat='%H%M%S',
        fromdate=datetime.datetime(2013, 10, 1),
        todate=datetime.datetime(2022, 12, 30))

    cerebro.adddata(data)  # Привязываем исторические данные

    cerebro.broker.setcash(10000.0)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()

    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot()
