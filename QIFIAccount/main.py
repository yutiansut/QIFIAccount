import datetime
import json

import click
from qaenv import mongo_ip
from QAPUBSUB import producer

from QIFIAccount.QARealtimeStockSim import QIFI_StockSIM_Account
from QUANTAXIS.QAUtil.QAParameter import (EXCHANGE_ID, MARKET_TYPE,
                                          ORDER_DIRECTION)


@click.command()
@click.option('--user')
@click.option('--password')
@click.option('--eventmq_ip', default='192.168.2.117')
@click.option('--eventmq_port', default=5672)
@click.option('--trade_host', default=mongo_ip)
def qasimStock(user, password, eventmq_ip, eventmq_port, trade_host):
    acc = QIFI_StockSIM_Account(username=user, password=password, eventmq_ip=eventmq_ip,
                                eventmq_port=eventmq_port, trade_host=trade_host)
    acc.initial()

    acc.log(acc.message)

    while 1:
        pass


@click.command()
@click.option('--user')
@click.option('--eventmq_ip', default='192.168.2.117')
@click.option('--eventmq_port', default=5672)
@click.option('--code', default='000001')
@click.option('--price', default=20)
@click.option('--amount', default=100)
@click.option('--towards', default='BUY')
def qasimstock_sendorder(user, eventmq_ip, eventmq_port, code, price, amount, towards):
    p = producer.publisher_routing(
        user='admin', password='admin', host=eventmq_ip, port=eventmq_port, exchange='QAORDER_ROUTER')

    p.pub(json.dumps({
        'topic': 'sendorder',
        'account_cookie': user,
        'strategy_id': 'test',
        'code': code,
        'price': price,
        'order_direction': towards,
        'order_offset': 'OPEN',
        'volume': amount,
        'order_time': str(datetime.datetime.now()),
        'exchange_id': 'test'
    }), routing_key=user)
