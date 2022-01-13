import datetime
import backtrader as bt


if __name__ == '__main__':
    cerebro = bt.Cerebro()

    # Create a Data Feed
    data = bt.feeds.GenericCSVData(
        dataname='FXIT_130101_220101.txt',
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
        fromdate=datetime.datetime(2013, 10, 30),
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
