from QAPUBSUB import producer
import json
import datetime

import click



def test_send_order(host='192.168.2.117'):
    p = producer.publisher_routing(
        user='admin', password='admin', host=host, exchange='QAORDER_ROUTER')

    price = {'000766': 5.81, '002038': 12.14, '002880':63.55, '300236': 58.67}
    for acc in ['userx']:

        for code in price.keys():
            p.pub(json.dumps({
                'topic': 'sendorder',
                'account_cookie': acc,
                'strategy_id': 'test',
                'code': code,
                'price': price[code],
                'order_direction': 'BUY',
                'order_offset': 'OPEN',
                'volume': 1000,
                'order_time': str(datetime.datetime.now()),
                'exchange_id': 'SH'
            }), routing_key=acc)

        # 撤单
        # p.pub(json.dumps({
        #     'topic': 'cancel_order',
        #     'order_id': "63da3715-eaeb-45de-95a4-ae6ca0f4700f",
        #     'account_cookie': acc
        # }), routing_key=acc)

if __name__ == "__main__":
    test_send_order()