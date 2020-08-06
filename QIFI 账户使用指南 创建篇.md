# QIFI ACCOUNT TEST

<!-- TOC -->

- [QIFI ACCOUNT TEST](#qifi-account-test)
    - [创建一个新的账户](#%E5%88%9B%E5%BB%BA%E4%B8%80%E4%B8%AA%E6%96%B0%E7%9A%84%E8%B4%A6%E6%88%B7)
    - [创建完账户后的一些基础查询/准备](#%E5%88%9B%E5%BB%BA%E5%AE%8C%E8%B4%A6%E6%88%B7%E5%90%8E%E7%9A%84%E4%B8%80%E4%BA%9B%E5%9F%BA%E7%A1%80%E6%9F%A5%E8%AF%A2%E5%87%86%E5%A4%87)
        - [查询持仓](#%E6%9F%A5%E8%AF%A2%E6%8C%81%E4%BB%93)
        - [查询订单](#%E6%9F%A5%E8%AF%A2%E8%AE%A2%E5%8D%95)
        - [查询成交](#%E6%9F%A5%E8%AF%A2%E6%88%90%E4%BA%A4)
        - [查询银行](#%E6%9F%A5%E8%AF%A2%E9%93%B6%E8%A1%8C)
        - [查询账户表](#%E6%9F%A5%E8%AF%A2%E8%B4%A6%E6%88%B7%E8%A1%A8)
        - [账户的标准化信息 QIFI](#%E8%B4%A6%E6%88%B7%E7%9A%84%E6%A0%87%E5%87%86%E5%8C%96%E4%BF%A1%E6%81%AF-qifi)
        - [查询当前时间](#%E6%9F%A5%E8%AF%A2%E5%BD%93%E5%89%8D%E6%97%B6%E9%97%B4)
    - [下单动作](#%E4%B8%8B%E5%8D%95%E5%8A%A8%E4%BD%9C)
        - [发送订单](#%E5%8F%91%E9%80%81%E8%AE%A2%E5%8D%95)
        - [撮合订单](#%E6%92%AE%E5%90%88%E8%AE%A2%E5%8D%95)

<!-- /TOC -->
QIFI 账户是 QUANTAXIS 的下一代标准化的账户系统, 因为 QAPOSITION 的方式可以快速的兼容多个场景下的账户标准, 并进行统一

QIFI 账户没有太多股票还是期货的概念, 一切持仓的行为都交给 QAPosition 来自动处理和识别, 我们首先进行账户的引入


## 创建一个新的账户

```python
from QIFIAccount import QIFI_Account, ORDER_DIRECTION
```

创建一个账户也非常的简单, 我们直接实例化这个账户即可, 需要注意的是, 账户的 username, password 是不可以重复的

```python
myacc =  QIFI_Account(username='myacc1', password='myacc1', model= "BACKTEST")
```

以下是账户实例化的时候的参数, 其中, model 指的是账户的运行类别:

- SIM => 实时模拟账户
- BACKTEST => 回测
- REAL => 实盘账户

broker_name 指的是经纪商, 一般来说只有实时的时候会需要用到, 如期货的期货公司, 股票账户的券商, 模拟的 QAPaperTrading, 方便进行数据查询

trade_host 指的是数据库的 ip 地址, QIFI 使用 mongodb 进行存储, 在 docker 内部你可以直接使用'mgdb'的 dns 形式访问

init_cash 指的是账户的初始化资金

```python
QIFI_Account(
    username,
    password,
    model='SIM',
    broker_name='QAPaperTrading',
    trade_host='mgdb',
    init_cash=1000000,
    taskid='7b4fe76a-97e1-4b3e-b8b9-be9ddb6e1c44',
)
```

在示例化账户以后, 你需要 initial来初始化账户, 在 initial 的过程中, 我们会从数据库中查询此账户, 如果账户之前有数据, 我们会直接将其reload 出来, 自动恢复账户的状态. 如果数据库中没有该账户, 我们则会构建新的账户,并进行存储.

```python
myacc.initial()
```

## 创建完账户后的一些基础查询/准备

我们已经通过 initial 初始化了一个账户, 现在我们来查看下账户的基础信息

### 查询持仓

```python
print('持仓')
print(myacc.positions)
```

持仓

{}

### 查询订单

```python
print('订单')
print(myacc.orders)
```

订单

{}


### 查询成交
```python
print('成交单')
print(myacc.trades)
```

成交单

{}


### 查询银行

```python
print('银行信息')
print(myacc.banks)
```

银行信息

{'QASIM': {'id': 'QASIM', 'name': 'QASIMBank', 'bank_account': '', 'fetch_amount': 0.0, 'qry_count': 0}}

### 查询账户表

```python
print('账户基础信息')
print(myacc.account_msg)


print('账户基础信息中包含了账户需要的所有数据, 具体可以参见 qifi 协议')
```

    账户基础信息
    {'user_id': 'myacc1', 'currency': 'CNY', 'pre_balance': 0, 'deposit': 1000000, 'withdraw': 0, 'WithdrawQuota': 0, 'close_profit': 0, 'commission': 0, 'premium': 0, 'static_balance': 0, 'position_profit': 0, 'float_profit': 0, 'balance': 1000000, 'margin': 0, 'frozen_margin': 0, 'frozen_commission': 0.0, 'frozen_premium': 0.0, 'available': 1000000, 'risk_ratio': 0.0}
    账户基础信息中包含了账户需要的所有数据, 具体可以参见 qifi 协议


### 账户的标准化信息 QIFI

当我们需要知道账户的信息时, 我们只需要快速的去重新执行myacc.account_msg, 账户会惰性计算, 而当我们需要完整的账户切面, 我们会返回一个 QIFI SLICE


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

### 查询当前时间


```python
print('在实时模拟中, 获取最新的时间采用的是:')

myacc.dtstr
```

在实时模拟中, 获取最新的时间采用的是:

'2020-08-06 00:56:02_131258'



现在你已经有了一个基础的了解, 让我们继续往下看

## 下单动作

### 发送订单
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



