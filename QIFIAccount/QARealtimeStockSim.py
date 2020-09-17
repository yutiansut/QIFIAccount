#
import datetime
import json
import threading
import uuid

import pymongo
from qaenv import eventmq_ip, eventmq_port, mongo_ip
from QAPUBSUB import producer
from QAPUBSUB.consumer import subscriber_routing, subscriber_topic

from QIFIAccount.QAQIFIAccount import QIFI_Account


class QIFI_StockSIM_Account(QIFI_Account):
    def __init__(self, username, password, model="SIM", broker_name="QAPaperTrading", trade_host=mongo_ip, init_cash=1000000,
                 eventmq_ip=eventmq_ip, eventmq_port=eventmq_port):
        super().__init__(username, password, model, broker_name, trade_host, init_cash)



        self.pub = producer.publisher_routing(
            exchange='qamdgateway', host=eventmq_ip, port=eventmq_port, durable=True)
        self.subrealtime = subscriber_topic(
            host=eventmq_ip, port=eventmq_port, exchange='QASMG', routing_key=username)

        self.ordersub = subscriber_routing(
            host=eventmq_ip, port=eventmq_port, exchange='QAORDER_ROUTER', routing_key=username)

        self.subrealtime.callback = self.realtime_data_callback
        self.ordersub.callback = self.listen_order_callback

        threading.Thread(target=self.subrealtime.start).start()
        threading.Thread(target=self.ordersub.start).start()

        self.pub_acc = producer.publisher_topic(
            exchange='qaStandardAcc', host=eventmq_ip, port=eventmq_port,  durable=True)

    def realtime_data_callback(self, a, b, c, data):
        data = json.loads(data)
        self.on_price_change(data['code'][2:], price=float(data['close']))

    def ask_subscribe(self, code):
        self.pub.pub(json.dumps({'account_cookie': self.username,
                                 'code': code}), routing_key='All')

    def on_ordersend(self, order):
        self.ask_subscribe(order['instrument_id'])

    def listen_order_callback(self, a, b, c, data):
        data = json.loads(data)
        if data['order_direction'] == 'BUY' and data['order_offset'] == 'OPEN':
            towards = 2
        elif data['order_direction'] == 'SELL' and data['order_offset'] == 'OPEN':
            towards = -2
        elif data['order_direction'] == 'SELL' and data['order_offset'] == 'CLOSE':
            towards = -3
        elif data['order_direction'] == 'BUY' and data['order_offset'] == 'CLOSE':
            towards = 3
        
        r = self.send_order(data['code'], data['volume'],
                            float(data['price']), towards)

        self.receive_deal(r['instrument_id'], r['price'], r['volume'], r['towards'], str(
            datetime.datetime.now()), order_id=r['order_id'], trade_id=str(uuid.uuid4()))

    def on_sync(self):
        self.pub_acc.pub(json.dumps(self.message), routing_key=self.username)

    def on_reload(self):
        for item in self.positions.keys():
            self.ask_subscribe(item)


if __name__ == '__main__':

    from QUANTAXIS.QAUtil.QAParameter import (
        EXCHANGE_ID,
        MARKET_TYPE,
        ORDER_DIRECTION)
    acc = QIFI_StockSIM_Account('userx1', 'userx1',
                                eventmq_ip='192.168.2.117', eventmq_port=5672)

    acc.initial()

    acc.log(acc.message)

    while 1:
        pass
