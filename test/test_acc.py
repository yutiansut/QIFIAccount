from QIFIAccount.QAQIFIAccount import QIFI_Account

def test_acc():
    acc = QIFI_Account('admin', 'admin', model='BACKTEST', init_cash=10000000)


    assert acc.init_cash==10000000

    