# QIFIAccount
QIFI协议下的Account实现

_QIFIAccount兼容 [QIFI协议标准](https://github.com/QUANTAXIS/QIFI/blob/master/README.md)_

```
pip install qifiaccount
```

```python

from qifiaccount import QIFI_Account
acc = QIFI_Account("x1", "x1")
acc.initial()


print(acc.message)


acc.send_order


acc.cancel_order


acc.get_position


```