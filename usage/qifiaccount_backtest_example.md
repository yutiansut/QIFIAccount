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




    '2020-12-23 23:58:07_925428'




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
    下单成功 898d56d3-5d48-4f4f-95b9-dcffba015d39



```python
import uuid
myacc.make_deal(order)
```

    全部成交 898d56d3-5d48-4f4f-95b9-dcffba015d39
    update trade



```python
myacc.positions
```




    {'stock_cn.000001': < QAPOSITION stock_cn.000001 amount 100/0 >}




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




    {'stock_cn.000001': < QAPOSITION stock_cn.000001 amount 100/0 >}




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


