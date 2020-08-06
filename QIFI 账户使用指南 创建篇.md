## QIFI ACCOUNT TEST


```python
from QIFIAccount import QIFI_Account, ORDER_DIRECTION
```


```python
QIFI_Account?
```

Initial
QIFI Account是一个基于 DIFF/ QIFI/ QAAccount后的一个实盘适用的Account基类


1. 兼容多持仓组合
2. 动态计算权益

使用 model = SIM/ REAL来切换

qifiaccount 不去区分你的持仓是股票还是期货, 因此你可以实现跨市场的交易持仓管理




```python
myacc =  QIFI_Account(username='myacc1', password='myacc1')
```


```python
myacc.initial()
```

### Create new Account

我们已经通过 initial 初始化了一个账户, 现在我们来查看下账户的基础信息



```python
print('持仓')
print(myacc.positions)
```

持仓

{}



```python
print('订单')
print(myacc.orders)
```

订单

{}



```python
print('成交单')
print(myacc.trades)
```

成交单

{}



```python
print('银行信息')
print(myacc.banks)
```

银行信息

{'QASIM': {'id': 'QASIM', 'name': 'QASIMBank', 'bank_account': '', 'fetch_amount': 0.0, 'qry_count': 0}}



```python
print('账户基础信息')
print(myacc.account_msg)


print('账户基础信息中包含了账户需要的所有数据, 具体可以参见 qifi 协议')
```

    账户基础信息
    {'user_id': 'myacc1', 'currency': 'CNY', 'pre_balance': 0, 'deposit': 1000000, 'withdraw': 0, 'WithdrawQuota': 0, 'close_profit': 0, 'commission': 0, 'premium': 0, 'static_balance': 0, 'position_profit': 0, 'float_profit': 0, 'balance': 1000000, 'margin': 0, 'frozen_margin': 0, 'frozen_commission': 0.0, 'frozen_premium': 0.0, 'available': 1000000, 'risk_ratio': 0.0}
    账户基础信息中包含了账户需要的所有数据, 具体可以参见 qifi 协议


### 当我们需要知道账户的信息时, 我们只需要快速的去重新执行myacc.account_msg, 账户会惰性计算, 而当我们需要完整的账户切面, 我们会返回一个 QIFI SLICE


```python
myacc.message
```




    {'account_cookie': 'myacc1',
     'password': 'myacc1',
     'databaseip': '',
     'model': 'SIM',
     'ping_gap': 5,
     'portfolio': 'QAPaperTrade',
     'broker_name': 'QAPaperTrading',
     'capital_password': '',
     'bank_password': '',
     'bankid': 'QASIM',
     'investor_name': '',
     'money': 1000000,
     'pub_host': '',
     'trade_host': '',
     'taskid': '7b4fe76a-97e1-4b3e-b8b9-be9ddb6e1c44',
     'sourceid': 'QIFI_Account',
     'updatetime': '',
     'wsuri': 'ws://www.yutiansut.com:7988',
     'bankname': 'QASIMBank',
     'trading_day': '2020-08-06',
     'status': 200,
     'accounts': {'user_id': 'myacc1',
      'currency': 'CNY',
      'pre_balance': 0,
      'deposit': 1000000,
      'withdraw': 0,
      'WithdrawQuota': 0,
      'close_profit': 0,
      'commission': 0,
      'premium': 0,
      'static_balance': 0,
      'position_profit': 0,
      'float_profit': 0,
      'balance': 1000000,
      'margin': 0,
      'frozen_margin': 0,
      'frozen_commission': 0.0,
      'frozen_premium': 0.0,
      'available': 1000000,
      'risk_ratio': 0.0},
     'trades': {},
     'positions': {},
     'orders': {},
     'event': {'2020-08-06 00:50:30_529556': '转账成功 1000000'},
     'transfers': {'0': {'datetime': 433241234123,
       'currency': 'CNY',
       'amount': 1000000,
       'error_id': 0,
       'error_msg': '成功'}},
     'banks': {'QASIM': {'id': 'QASIM',
       'name': 'QASIMBank',
       'bank_account': '',
       'fetch_amount': 0.0,
       'qry_count': 0}},
     'frozen': {},
     'settlement': {}}




```python
print('在实时模拟中, 获取最新的时间采用的是:')

myacc.dtstr
```

在实时模拟中, 获取最新的时间采用的是:

'2020-08-06 00:56:02_131258'



现在你已经有了一个基础的了解, 让我们继续往下看

## 下单函数


```python
  
r = myacc.send_order('000001', 10, 12, ORDER_DIRECTION.BUY)

```

    {'volume_long': 0, 'volume_short': 0, 'volume_long_frozen': 0, 'volume_short_frozen': 0}
    {'volume_long': 0, 'volume_short': 0}
    order check success
    下单成功 04e6e2c0-61dc-4d04-bca0-97bced2956b1



```python
myacc.orders
```




    {'04e6e2c0-61dc-4d04-bca0-97bced2956b1': {'account_cookie': 'myacc1',
      'user_id': 'myacc1',
      'instrument_id': '000001',
      'towards': 1,
      'exchange_id': None,
      'order_time': '2020-08-06 00:57:39_053237',
      'volume': 10,
      'price': 12.0,
      'order_id': '04e6e2c0-61dc-4d04-bca0-97bced2956b1',
      'seqno': 1,
      'direction': 'BUY',
      'offset': '',
      'volume_orign': 10,
      'price_type': 'LIMIT',
      'limit_price': 12.0,
      'time_condition': 'GFD',
      'volume_condition': 'ANY',
      'insert_date_time': 1.596646659052434e+18,
      'exchange_order_id': '2ba5fba7-c8cb-4d59-8074-24cd3c7b6e78',
      'status': 'ALIVE',
      'volume_left': 10,
      'last_msg': '已报'}}




```python
myacc.trades
```




    {}



### 撮合订单


```python
import uuid
myacc.receive_deal(r['instrument_id'], 11.8, r['volume'], r['towards'],
                  myacc.dtstr, order_id=r['order_id'], trade_id=str(uuid.uuid4()))

```

全部成交 04e6e2c0-61dc-4d04-bca0-97bced2956b1
update trade



```python
myacc.trades

    {'58f04d40-c126-4539-9a6b-06b5c5a09c79': {'seqno': 2,
        'user_id': 'myacc1',
        'trade_id': '58f04d40-c126-4539-9a6b-06b5c5a09c79',
        'exchange_id': None,
        'instrument_id': '000001',
        'order_id': '04e6e2c0-61dc-4d04-bca0-97bced2956b1',
        'exchange_trade_id': '58f04d40-c126-4539-9a6b-06b5c5a09c79',
        'direction': 'BUY',
        'offset': '',
        'volume': 10,
        'price': 11.8,
        'trade_time': '2020-08-06 00:58:41_440478',
        'commission': 0.0,
        'trade_date_time': 1.5966467214404782e+18}}

```


```python
myacc.orders

    {'04e6e2c0-61dc-4d04-bca0-97bced2956b1': {'account_cookie': 'myacc1',
      'user_id': 'myacc1',
      'instrument_id': '000001',
      'towards': 1,
      'exchange_id': None,
      'order_time': '2020-08-06 00:57:39_053237',
      'volume': 10,
      'price': 12.0,
      'order_id': '04e6e2c0-61dc-4d04-bca0-97bced2956b1',
      'seqno': 1,
      'direction': 'BUY',
      'offset': '',
      'volume_orign': 10,
      'price_type': 'LIMIT',
      'limit_price': 12.0,
      'time_condition': 'GFD',
      'volume_condition': 'ANY',
      'insert_date_time': 1.596646659052434e+18,
      'exchange_order_id': '2ba5fba7-c8cb-4d59-8074-24cd3c7b6e78',
      'status': 'FINISHED',
      'volume_left': 0,
      'last_msg': '全部成交'}}
```



