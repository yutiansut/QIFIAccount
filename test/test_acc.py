from QIFIAccount.QAQIFIAccount import QIFI_Account, ORDER_DIRECTION


def test_acc():
    myacc = QIFI_Account('myacc1', 'myacc1', model='BACKTEST',
                         init_cash=10000000, nodatabase=True)

    assert myacc.init_cash == 10000000
    myacc.initial()
    assert(myacc.positions == {})

    assert(myacc.trading_day == '')

    order = myacc.send_order(
        '000001', 100, 12, ORDER_DIRECTION.BUY, datetime='2020-01-01')
    assert(order == {'account_cookie': 'myacc1',
                     'user_id': 'myacc1',
                     'instrument_id': '000001',
                     'towards': 1,
                     'exchange_id': 'stock_cn',
                     'order_time': order['order_time'],
                     'volume': 100,
                     'price': 12.0,
                     'order_id': order['order_id'],
                     'seqno': 1,
                     'direction': 'BUY',
                     'offset': 'OPEN',
                     'volume_orign': 100,
                     'price_type': 'LIMIT',
                     'limit_price': 12.0,
                     'time_condition': 'GFD',
                     'volume_condition': 'ANY',
                     'insert_date_time': order['insert_date_time'],
                     'exchange_order_id': order['exchange_order_id'],
                     'status': 'ALIVE',
                     'volume_left': 100,
                     'last_msg': '已报'})

    assert(list(myacc.positions.keys()) == ['stock_cn.000001'])
    position_000001 = myacc.get_position('000001')
    assert(position_000001.volume_long == 0)
    print('钱在下单后进入frozen 冻结住')
    assert(myacc.available == 9998800.0)
    assert(list(myacc.frozen.values()) == [{'amount': 100,
                                            'coeff': 12.0,
                                            'money': 1200.0}])

    print('试图撮合')

    myacc.make_deal(order)

    assert(myacc.positions['stock_cn.000001'].volume_long == 100)

    assert(list(myacc.frozen.values()) == [{'amount': 0,
                                            'coeff': 12.0,
                                            'money': 0}])
    assert(myacc.get_position('stock_cn.000001').last_price == 12.0)
    assert(myacc.get_position('stock_cn.000001').open_cost_long == 1200.0)

    myacc.on_price_change('000001', 13, '2020-01-01')
    assert(myacc.datetime == '2020-01-01')
    assert(myacc.float_profit == 100.0)
    assert(myacc.balance == 10000100.0)
    assert(myacc.get_position('000001').message == {'code': '000001',
                                                  'instrument_id': '000001',
                                                  'user_id': 'quantaxis',
                                                  'portfolio_cookie': 'portfolio',
                                                  'username': 'quantaxis',
                                                  'position_id': myacc.get_position('000001').position_id,
                                                  'account_cookie': 'quantaxis',
                                                  'frozen': {},
                                                  'name': None,
                                                  'spms_id': None,
                                                  'oms_id': None,
                                                  'market_type': 'stock_cn',
                                                  'exchange_id': 'stock_cn',
                                                  'moneypreset': 100000,
                                                  'moneypresetLeft': 98800.0,
                                                  'lastupdatetime': '',
                                                  'volume_long_today': 100,
                                                  'volume_long_his': 0,
                                                  'volume_long': 100,
                                                  'volume_long_yd': 0,
                                                  'volume_short_yd': 0,
                                                  'volume_short_today': 0,
                                                  'volume_short_his': 0,
                                                  'volume_short': 0,
                                                  'pos_long_his': 0,
                                                  'pos_long_today': 100,
                                                  'pos_short_his': 0,
                                                  'pos_short_today': 0,
                                                  'volume_long_frozen_today': 0,
                                                  'volume_long_frozen_his': 0,
                                                  'volume_long_frozen': 0,
                                                  'volume_short_frozen_today': 0,
                                                  'volume_short_frozen_his': 0,
                                                  'volume_short_frozen': 0,
                                                  'margin_long': 1200.0,
                                                  'margin_short': 0,
                                                  'margin': 1200.0,
                                                  'position_price_long': 12.0,
                                                  'position_cost_long': 1200.0,
                                                  'position_price_short': 0,
                                                  'position_cost_short': 0.0,
                                                  'open_price_long': 12.0,
                                                  'open_cost_long': 1200.0,
                                                  'open_price_short': 0,
                                                  'open_cost_short': 0.0,
                                                  'trades': [],
                                                  'orders': {},
                                                  'last_price': 13,
                                                  'float_profit_long': 100.0,
                                                  'float_profit_short': 0.0,
                                                  'float_profit': 100.0,
                                                  'position_profit_long': 100.0,
                                                  'position_profit_short': 0.0,
                                                  'position_profit': 100.0})
