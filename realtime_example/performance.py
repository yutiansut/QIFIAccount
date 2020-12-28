from collections import deque

import pymongo
import pandas as pd
import QUANTAXIS as QA



def get_multipleacc(account):
    client =  pymongo.MongoClient('192.168.2.117').QAREALTIME.account
    res  =  [item['trades']  for item in client.find({'account_cookie': {"$regex":"{}*".format(account)}})]
    x1 = []
    for i in res:
        if len(i) >0:
            x1.extend(i.values())
    bx = pd.DataFrame(x1)
    bx = bx.assign(datetime =  pd.to_datetime(bx.trade_date_time.apply(QA.QA_util_stamp2datetime)), code = bx.instrument_id, direction=(bx.direction+ bx.offset).apply(lambda x: 2 if x=='BUYOPEN' else -3), amount= bx.volume)
    return bx
def pnl_fifo(trades):
    
    #从QUANTAXIS抽离出来 兼容QIFI的账户配对
    market_preset = QA.QAARP.MARKET_PRESET()

    codes = list(set(trades.code.to_list()))
    X = dict(
        zip(
            codes,
            [{'buy': deque(), 'sell': deque()}
             for i in range(len(codes))]
        )
    )
    pair_table = []
    for _, data in trades.iterrows():
        if abs(data.amount) < 1:
            pass
        else:
            while True:
                try:
                    if data.direction in[1, 2, -2]:
                        if data.direction in [1, 2]:
                            X[data.code]['buy'].append(
                                (data.datetime,
                                 data.amount,
                                 data.price,
                                 data.direction)
                            )
                        elif data.direction in [-2]:
                            X[data.code]['sell'].append(
                                (data.datetime,
                                 data.amount,
                                 data.price,
                                 data.direction)
                            )
                        break
                    elif data.direction in[-1, 3, -3]:

                        rawoffset = 'buy' if data.direction in [
                            -1, -3] else 'sell'

                        l = X[data.code][rawoffset].popleft()
                        if abs(l[1]) > abs(data.amount):
                            """
                            if raw> new_close:
                            """
                            temp = (l[0], l[1] + data.amount, l[2])
                            X[data.code][rawoffset].appendleft(temp)
                            if data.amount < 0:
                                pair_table.append(
                                    [
                                        data.code,
                                        data.datetime,
                                        l[0],
                                        abs(data.amount),
                                        data.price,
                                        l[2],
                                        rawoffset
                                    ]
                                )
                                break
                            else:
                                pair_table.append(
                                    [
                                        data.code,
                                        l[0],
                                        data.datetime,
                                        abs(data.amount),
                                        l[2],
                                        data.price,
                                        rawoffset
                                    ]
                                )
                                break

                        elif abs(l[1]) < abs(data.amount):
                            data.amount = data.amount + l[1]

                            if data.amount < 0:
                                pair_table.append(
                                    [
                                        data.code,
                                        data.datetime,
                                        l[0],
                                        l[1],
                                        data.price,
                                        l[2],
                                        rawoffset
                                    ]
                                )
                            else:
                                pair_table.append(
                                    [
                                        data.code,
                                        l[0],
                                        data.datetime,
                                        l[1],
                                        l[2],
                                        data.price,
                                        rawoffset
                                    ]
                                )
                        else:
                            if data.amount < 0:
                                pair_table.append(
                                    [
                                        data.code,
                                        data.datetime,
                                        l[0],
                                        abs(data.amount),
                                        data.price,
                                        l[2],
                                        rawoffset
                                    ]
                                )
                                break
                            else:
                                pair_table.append(
                                    [
                                        data.code,
                                        l[0],
                                        data.datetime,
                                        abs(data.amount),
                                        l[2],
                                        data.price,
                                        rawoffset
                                    ]
                                )
                                break
                except:
                    break

    pair_title = [
        'code',
        'buy_date',
        'sell_date',

        'amount',
        'buy_price',
        'sell_price',

        'rawdirection'
    ]
    pnl = pd.DataFrame(pair_table, columns=pair_title)

    pnl = pnl.assign(
        unit=pnl.code.apply(lambda x: market_preset.get_unit(x)),
        pnl_ratio=(pnl.sell_price / pnl.buy_price) - 1,
        sell_date=pd.to_datetime(pnl.sell_date),
        buy_date=pd.to_datetime(pnl.buy_date)
    )
    pnl = pnl.assign(
        pnl_money=(pnl.sell_price - pnl.buy_price) * pnl.amount * pnl.unit,
        hold_gap=abs(pnl.sell_date - pnl.buy_date),
        if_buyopen=pnl.rawdirection == 'buy'
    )
    pnl = pnl.assign(
        openprice=pnl.if_buyopen.apply(lambda pnl: 1 if pnl else 0) *
        pnl.buy_price +
        pnl.if_buyopen.apply(lambda pnl: 0 if pnl else 1) * pnl.sell_price,
        opendate=pnl.if_buyopen.apply(lambda pnl: 1 if pnl else 0) *
        pnl.buy_date.map(str) +
        pnl.if_buyopen.apply(lambda pnl: 0 if pnl else 1) *
        pnl.sell_date.map(str),
        closeprice=pnl.if_buyopen.apply(lambda pnl: 0 if pnl else 1) *
        pnl.buy_price +
        pnl.if_buyopen.apply(lambda pnl: 1 if pnl else 0) * pnl.sell_price,
        closedate=pnl.if_buyopen.apply(lambda pnl: 0 if pnl else 1) *
        pnl.buy_date.map(str) +
        pnl.if_buyopen.apply(lambda pnl: 1 if pnl else 0) *
        pnl.sell_date.map(str)
    )
    return pnl.set_index('code')


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    trade= get_multipleacc("Cw")
    res = pnl_fifo(trade)



