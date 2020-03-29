import datetime
import json
import time

import click
from QAPUBSUB import producer


def test_send_order(host='192.168.2.117'):
    p = producer.publisher_routing(
        user='admin', password='admin', host=host, exchange='QAORDER_ROUTER')

    ulist = [

    {'code': '300078', 'price': 13.25},
    {'code': '601966', 'price': 19.03},
    {'code': '601163', 'price': 12.81},
    {'code': '600469', 'price': 4.93},
    {'code': '000589', 'price': 3.81},
    {'code': '601500', 'price': 5.63},
    {'code': '000599', 'price': 3.78},
    {'code': '600048', 'price': 13.97},
    {'code': '000002', 'price': 24.51},
    {'code': '000671', 'price': 6.39},
    {'code': '600383', 'price': 12.14},
    {'code': '000961', 'price': 7.01},
    {'code': '600466', 'price': 5.76},
    {'code': '600325', 'price': 6.06},
    {'code': '002146', 'price': 7.25}]
    for acc in ['jf1']:

        for x in ulist:
            p.pub(json.dumps({
                'topic': 'sendorder',
                'account_cookie': acc,
                'strategy_id': 'test',
                'code': x['code'],
                'price': x['price'],
                'order_direction': 'BUY',
                'order_offset': 'OPEN',
                'volume': 100,
                'order_time': str(datetime.datetime.now()),
                'exchange_id': 'SH'
            }), routing_key=acc)
            time.sleep(10)

        # 撤单
        # p.pub(json.dumps({
        #     'topic': 'cancel_order',
        #     'order_id': "63da3715-eaeb-45de-95a4-ae6ca0f4700f",
        #     'account_cookie': acc
        # }), routing_key=acc)


if __name__ == "__main__":
    test_send_order()
