# QIFIAccount
QIFI协议下的Account实现

_QIFIAccount兼容 [QIFI协议标准](https://github.com/QUANTAXIS/QIFI/blob/master/README.md)和[DIFF协议标准](https://github.com/shinnytech/diff)_

```
pip install qifiaccount
```


### 用法:

参见 /usage 文件夹下的ipython notebook

```python

from QIFIAccount import QIFI_Account, ORDER_DIRECTION
acc = QIFI_Account("x1", "x1")
acc.initial()


print(acc.message)


acc.send_order


acc.cancel_order


acc.get_position


```
