from QAPUBSUB import producer
import json
import datetime

import click


def test_send_order(host='192.168.2.117'):
    p = producer.publisher_routing(
        user='admin', password='admin', host=host, exchange='QAORDER_ROUTER')

    price = {
            # '000766': {
            #     'price': 5.81,
            #     'amount': 2000},
            # '002038': {
            #     'price': 12.15,
            #     'amount': 2000},
            # '002880': {
            #     'price': 63.64,
            #     'amount': 200}, 
            '300236': {
                'price': 67.54, 
                'amount': 700}}
    for acc in ['userx1']:

        for code in price.keys():
            p.pub(json.dumps({
                'topic': 'sendorder',
                'account_cookie': acc,
                'strategy_id': 'test',
                'code': code,
                'price': price[code]['price'],
                'order_direction': 'BUY',
                'order_offset': 'OPEN',
                'volume': price[code]['amount'],
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
