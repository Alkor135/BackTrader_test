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
        self.increment_is_completed = False  # True - приращение в этом месяце 'выполнено'
        # self.data_open = self.datas[0].open
        # self.data_high = self.datas[0].high
        # self.data_low = self.datas[0].low
        self.data_close = self.datas[0].close
        # self.data_volume = self.datas[0].volume
        self.order = None  # Заявка
        self.bar_executed = None  # Бар исполнения

    def notify_order(self, order):
        """ Изменение статуса заявки """
        if order.status in [order.Submitted, order.Accepted]:  # Если заявка не исполнена (заявка Отправлена/Принята)
            return  # Статус заявки не изменился, выходим

        if order.status in [order.Completed]:  # Если заявка исполнена
            if order.isbuy():  # Заявка на покупку
                self.log('BUY EXECUTED, %.2f' % order.executed.price)
            elif order.issell():  # Заявка на продажу
                self.log('SELL EXECUTED, %.2f' % order.executed.price)
            self.bar_executed = len(self)  # Номер бара на котором была исполнена заявка

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:  # Если заявка отменена/отклонена
            self.log('Order Canceled/Margin/Rejected')

        self.order = None  # Этой заявки больше нет

    def next(self):
        """ Приход нового бара """
        # Ежемесячное приращение капитала
        dt_1 = self.datas[0].datetime.datetime(-1)  # Дата время предыдущего бара
        dt0 = self.datas[0].datetime.datetime(0)  # Дата время текущего бара
        # Если месяц предыдущего бара не равен месяцу текущего бара
        if datetime.datetime.timetuple(dt_1)[1] != datetime.datetime.timetuple(dt0)[1]:
            self.increment_is_completed = False  # Статус приращения устанавливаем в 'не выполнено'
        if not self.increment_is_completed and increment_date <= datetime.datetime.timetuple(dt0)[2]:
            cerebro.broker.setcash(cerebro.broker.getvalue() + increment)
            self.increment_is_completed = True  # Статус приращения устанавливаем в 'выполнено'

        self.log('Close, %.2f' % self.data_close[0])

        if self.order:  # Если есть необработанная заявка, выходим
            return

        self.order = self.buy()  # Создание ордера на покупку


if __name__ == '__main__':
    increment = 10000.00  # Ежемесячное приращение
    increment_date = 15  # Дата приращения (число месяца)
    path_data = 'data/FXIT_130101_220101.txt'  # Путь и файл данных

    cerebro = bt.Cerebro()  # Инициализируем движок BackTrader
    cerebro.addsizer(bt.sizers.PercentSizer, percents=100)  # default sizer for strategies
    cerebro.addstrategy(TestStrategy)  # Привязываем торговую систему

    # Create a Data Feed
    data = bt.feeds.GenericCSVData(
        dataname=path_data,
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

    cerebro.broker.setcash(10000.0)  # Начальное значение Depo
    cerebro.broker.setcommission(commission=0.0006)  # 0.05% комиссия брокера ВТБ + 0.01% комиссия биржи

    print('Начальное значение Depo: %.2f' % cerebro.broker.getvalue())  # Вывод в консоль начальное значение Depo

    cerebro.run()  # Старт стратегии

    print('Конечное значение Depo: %.2f' % cerebro.broker.getvalue())  # Вывод в консоль конечное значение Depo
    cerebro.plot()  # Отображение графиков
