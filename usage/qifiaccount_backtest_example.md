```python
from QIFIAccount import QIFI_Account, ORDER_DIRECTION
```

    you are using non-interactive mdoel quantaxis



```python
myacc =  QIFI_Account(username='myacc1', password='myacc1', model="BACKTEST")
```


```python
myacc.initial()
```

    Create new Account



```python

print('持仓')
print(myacc.positions)
```

    持仓
    {}



```python
myacc.dtstr
```




    '2020-12-24 00:31:19_704695'




```python
myacc.datetime
```




    ''




```python
order = myacc.send_order('000001', 100, 12, ORDER_DIRECTION.BUY, datetime='2020-01-01')
```

    {'volume_long': 0, 'volume_short': 0, 'volume_long_frozen': 0, 'volume_short_frozen': 0}
    {'volume_long': 0, 'volume_short': 0}
    order check success
    下单成功 fb90a2e5-e89f-4d46-8d94-bd4f3bbc1d88



```python
import uuid
myacc.make_deal(order)
```

    全部成交 fb90a2e5-e89f-4d46-8d94-bd4f3bbc1d88
    update trade



```python
myacc.positions
```




    {'stock_cn.000001': < QAPOSITION 000001 amount 100/0 >}




```python
myacc.positions['stock_cn.000001'].volume_long
```




    100




```python
myacc.balance
```




    1000000.0




```python
myacc.get_position('stock_cn.000001').last_price
```




    12.0




```python
myacc.get_position('stock_cn.000001').open_cost_long
```




    1200.0




```python
myacc.datetime
```




    ''




```python
myacc.on_price_change('000001', 13, '2020-01-01')
#myacc.get_position('stock_cn.000001').message
```


```python
myacc.positions
```




    {'stock_cn.000001': < QAPOSITION 000001 amount 100/0 >}




```python
myacc.datetime
```




    '2020-01-01'




```python
myacc.float_profit
```




    100.0




```python
myacc.balance
```




    1000100.0




```python
order = myacc.send_order('RB2101', 1, 3800, ORDER_DIRECTION.BUY, datetime='2020-01-01')
```

    {'volume_long': 0, 'volume_short': 0, 'volume_long_frozen': 0, 'volume_short_frozen': 0}
    {'volume_long': 0, 'volume_short': 0}
    order check success
    下单成功 544459bf-c107-48a5-a98e-79f5411c46c8



```python
myacc.make_deal(order)
```

    全部成交 544459bf-c107-48a5-a98e-79f5411c46c8
    update trade



```python
myacc.positions
```




    {'stock_cn.000001': < QAPOSITION 000001 amount 100/0 >,
     'SHFE.RB2101': < QAPOSITION RB2101 amount 1/0 >}




```python
import QUANTAXIS as QA
```


```python
myacc.positions
```




    {'stock_cn.000001': < QAPOSITION 000001 amount 100/0 >,
     'SHFE.RB2101': < QAPOSITION RB2101 amount 1/0 >}




```python
myacc.on_price_change('RB2101', 3920, '2020-01-01')

```


```python

```


```python
myacc.float_profit
```




    1300.0




```python
myacc.get_position('RB2101').code#.open_cost_long
```




    'RB2101'




```python
myacc.get_position('RB2101').market_preset
```




    {'name': '螺纹钢',
     'unit_table': 10,
     'price_tick': 1.0,
     'buy_frozen_coeff': 0.09,
     'sell_frozen_coeff': 0.09,
     'exchange': 'SHFE',
     'commission_coeff_peramount': 0.0001,
     'commission_coeff_pervol': 0,
     'commission_coeff_today_peramount': 0.0001,
     'commission_coeff_today_pervol': 0}




```python
myacc.get_position('RB2101').code
```




    'RB2101'




```python
myacc.frozen
```




    {'fb90a2e5-e89f-4d46-8d94-bd4f3bbc1d88': {'amount': 0,
      'coeff': 12.0,
      'money': 0},
     '544459bf-c107-48a5-a98e-79f5411c46c8': {'amount': 0,
      'coeff': 3420.0,
      'money': 0}}


