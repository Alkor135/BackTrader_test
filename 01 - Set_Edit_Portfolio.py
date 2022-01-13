import backtrader as bt


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(1000.0)
    print(f'Стартовый капитал: {cerebro.broker.getvalue():.2f}')

    cerebro.broker.setcash(cerebro.broker.getvalue() + 100.00)
    print(cerebro.broker.cash)
    cerebro.run()
    cerebro.broker.setcash(cerebro.broker.getvalue() + 100.00)

    print(f'Конечный капитал: {cerebro.broker.getvalue():.2f}')
