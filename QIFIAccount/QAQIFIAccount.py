import datetime
import uuid
from QUANTAXIS.QAARP.market_preset import MARKET_PRESET
from QIFIAccount.QAPosition import QA_Position
import pymongo


class ORDER_DIRECTION():
    """订单的买卖方向

    BUY 股票 买入
    SELL 股票 卖出
    BUY_OPEN 期货 多开
    BUY_CLOSE 期货 空平(多头平旧仓)
    SELL_OPEN 期货 空开
    SELL_CLOSE 期货 多平(空头平旧仓)

    ASK  申购
    """

    BUY = 1
    SELL = -1
    BUY_OPEN = 2
    BUY_CLOSE = 3
    SELL_OPEN = -2
    SELL_CLOSE = -3
    SELL_CLOSETODAY = -4
    BUY_CLOSETODAY = 4
    ASK = 0
    XDXR = 5
    OTHER = 6


def parse_orderdirection(od):
    direction = ''
    offset = ''

    if od in [1, 2, 3]:
        direction = 'BUY'
    elif od in [-1, -2, -3]:
        direction = 'SELL'
    if abs(od) == 2:
        offset = 'OPEN'
    elif abs(od) == 3:
        offset = 'CLOSE'

    return direction, offset


class QIFI_Account():

    def __init__(self, username, password, model="SIM", broker_name="QAPaperTrading", trade_host='127.0.0.1'):
        """Initial
        QIFI Account是一个基于 DIFF/ QIFI/ QAAccount后的一个实盘适用的Account基类


        1. 兼容多持仓组合
        2. 动态计算权益

        使用 model = SIM/ REAL来切换


        """
        self.user_id = username
        self.username = username
        self.password = password

        self.source_id = "QIFI_Account"  # 识别号
        self.market_preset = MARKET_PRESET()
        # 指的是 Account所属的账户编组(实时的时候的账户观察组)
        self.portfolio = "QAPaperTrade"
        self.model = model

        self.broker_name = broker_name    # 所属期货公司/ 模拟的组
        self.investor_name = ""  # 账户所属人(实盘的开户人姓名)
        self.bank_password = ""
        self.capital_password = ""
        self.wsuri = ""

        self.bank_id = "QASIM"
        self.bankname = "QASIMBank"

        self.trade_host = trade_host
        self.db = pymongo.MongoClient(trade_host).QAREALTIME

        self.pub_host = ""
        self.trade_host = ""
        self.last_updatetime = ""
        self.status = 200
        self.trading_day = ""

        self.pre_balance = 0

        self.static_balance = 0

        self.deposit = 0  # 入金
        self.withdraw = 0  # 出金
        self.withdrawQuota = 0  # 可取金额
        self.close_profit = 0
        self.event_id = 0
        self.money = 0
        # QIFI 协议
        self.transfers = {}

        self.banks = {}

        self.frozen = {}

        self.events = {}
        self.positions = {}
        self.trades = {}
        self.orders = {}

    def initial(self):

        self.reload()

        if self.pre_balance == 0 and self.balance == 0 and self.model == "SIM":
            print('Create new Account')
            self.create_simaccount()

        self.sync()

    def reload(self):
        message = self.db.account.find_one(
            {'account_cookie': self.user_id, 'password': self.password})

        time = datetime.datetime.now()
        # resume/settle

        if time.hour <= 15:
            self.trading_day = time.date()
        else:
            if time.weekday() in [0, 1, 2, 3]:
                self.trading_day = time.date() + datetime.timedelta(days=1)
            elif time.weekday() in [4, 5, 6]:
                self.trading_day = time.date() + datetime.timedelta(days=(7-time.weekday()))
        if message is not None:
            accpart = message.get('accounts')

            self.money = message.get('money')
            self.source_id = message.get('sourceid')

            self.pre_balance = accpart.get('pre_balance')
            self.deposit = accpart.get('deposit')
            self.withdraw = accpart.get('withdraw')
            self.withdrawQuota = accpart.get('WithdrawQuota')
            self.close_profit = accpart.get('close_profit')
            self.static_balance = accpart.get('static_balance')
            self.events = message.get('events')
            self.trades = message.get('trades')
            self.transfers = message.get('transfers')
            self.orders = message.get('orders')
            self.banks = message.get('banks')

            self.status = message.get('status')
            self.wsuri = message.get('wsuri')

            positions = message.get('positions')
            for position in positions.values():
                self.positions[position.get('instrument_id')] = QA_Position(
                ).loadfrommessage(position)

            if message.get('trading_day', '') == str(self.trading_day):
                # reload
                pass

            else:
                # settle
                self.settle()

    def sync(self):
        print(self.message)
        self.db.account.update({'account_cookie': self.user_id, 'password': self.password}, {
            '$set': self.message}, upsert=True)
        self.db.hisaccount.insert_one(
            {'updatetime': self.dtstr, 'account_cookie': self.user_id, 'accounts': self.account_msg})

    def settle(self):
        print('settle')
        self.db.history.insert_one(self.message)
        self.pre_balance += (self.deposit - self.withdraw + self.close_profit)
        self.static_balance = self.pre_balance

        self.close_profit = 0
        self.deposit = 0  # 入金
        self.withdraw = 0  # 出金

        self.money += self.frozen_margin

        self.orders = {}
        self.frozen = {}
        self.trades = {}
        self.transfers = {}
        self.events = {}
        self.event_id = 0

        for item in self.positions.values():
            item.settle()

        self.sync()

    @property
    def dtstr(self):
        return str(datetime.datetime.now())

    def ask_deposit(self, money):

        self.deposit += money
        self.money += money
        self.transfers[str(self.event_id)] = {
            "datetime": 433241234123,  # // 转账时间, epoch nano
            "currency": "CNY",  # 币种
            "amount": money,  # 涉及金额
            "error_id": 0,  # 转账结果代码
            "error_msg": "成功",  # 转账结果代码
        }
        self.events[self.dtstr] = "转账成功 {}".format(money)

    def ask_withdraw(self, money):
        if self.withdrawQuota > money:
            self.withdrawQuota -= money
            self.withdraw += money
            self.transfers[str(self.event_id)] = {
                "datetime": 433241234123,  # // 转账时间, epoch nano
                "currency": "CNY",  # 币种
                "amount": -money,  # 涉及金额
                "error_id": 0,  # 转账结果代码
                "error_msg": "成功",  # 转账结果代码
            }
            self.events[self.dtstr] = "转账成功 {}".format(-money)
        else:
            self.events[self.dtstr] = "转账失败: 余额不足 left {}  ask {}".format(
                self.withdrawQuota, money)

    def create_simaccount(self):
        self.trading_day = str(datetime.date.today())
        self.wsuri = "ws://www.yutiansut.com:7988"
        self.pre_balance = 0
        self.static_balance = 0
        self.deposit = 0  # 入金
        self.withdraw = 0  # 出金
        self.withdrawQuota = 0  # 可取金额
        self.user_id = str(uuid.uuid4())
        self.password = str(uuid.uuid4())
        self.money = 0
        self.close_profit = 0
        self.event_id = 0
        self.transfers = {}
        self.banks = {}
        self.events = {}
        self.positions = {}
        self.trades = {}
        self.orders = {}
        self.banks[str(self.bank_id)] = {
            "id": self.bank_id,
            "name": self.bankname,
            "bank_account": "",
            "fetch_amount": 0.0,
            "qry_count": 0
        }
        self.ask_deposit(1000000)

    def add_position(self, position):

        if position.instrument_id not in self.positions.keys():
            self.positions[position.instrument_id] = position
            return 0
        else:
            return 1

    def drop_position(self, position):
        pass

    def log(self, message):
        self.events[self.dtstr] = message

    @property
    def message(self):
        return {
            # // 账户号(兼容QUANTAXIS QAAccount)// 实盘的时候是 账户id
            "account_cookie": self.user_id,
            "password": self.password,
            "databaseip": self.trade_host,
            "model": self.model,
            "ping_gap": 5,
            "portfolio": self.portfolio,
            "broker_name": self.broker_name,  # // 接入商名称
            "capital_password": self.capital_password,  # // 资金密码 (实盘用)
            "bank_password": self.bank_password,  # // 银行密码(实盘用)
            "bankid": self.bank_id,  # // 银行id
            "investor_name": self.investor_name,  # // 开户人名称
            "money": self.money,         # // 当前可用现金
            "pub_host": self.pub_host,
            "trade_host": self.trade_host,
            "taskid": "",
            "sourceid": self.source_id,
            "updatetime": str(self.last_updatetime),
            "wsuri": self.wsuri,
            "bankname": self.bankname,
            "trading_day": str(self.trading_day),
            "status": self.status,
            "accounts": self.account_msg,
            "trades": self.trades,
            "positions": self.position_msg,
            "orders": self.orders,
            "events": self.events,
            "transfers": self.transfers,
            "banks": self.banks,
            "settlement": {},
        }

    @property
    def account_msg(self):
        return {
            "user_id": self.user_id,
            "currency": "CNY",
            "pre_balance": self.pre_balance,
            "deposit": self.deposit,
            "withdraw": self.withdraw,
            "WithdrawQuota": self.withdrawQuota,
            "close_profit": self.close_profit,
            "commission": self.commission,
            "premium": self.premium,
            "static_balance": self.static_balance,
            "position_profit": self.position_profit,
            "float_profit": self.float_profit,
            "balance": self.balance,
            "margin": self.margin,
            "frozen_margin": self.frozen_margin,
            "frozen_commission": 0.0,
            "frozen_premium": 0.0,
            "available": self.available,
            "risk_ratio": 1 - self.available/self.balance
        }

    @property
    def position_msg(self):
        return dict(zip(self.positions.keys(), [item.message for item in self.positions.values()]))

    @property
    def position_profit(self):
        return sum([position.position_profit for position in self.positions.values()])

    @property
    def float_profit(self):
        return sum([position.float_profit for position in self.positions.values()])

    @property
    def frozen_margin(self):
        return sum([item.get('money') for item in self.frozen.values()])
# 惰性计算
    @property
    def available(self):
        return self.money

    @property
    def margin(self):
        """保证金
        """
        return sum([position.margin for position in self.positions.values()])

    @property
    def commission(self):
        return sum([position.commission for position in self.positions.values()])

    @property
    def premium(self):
        pass

    @property
    def balance(self):
        """动态权益

        Arguments:
            self {[type]} -- [description]
        """

        return self.static_balance + self.deposit - self.withdraw + self.float_profit + self.close_profit

    def order_check(self, code: str, amount: float, price: float, towards: int, order_id: str) -> bool:
        res = False
        qapos = self.get_position(code)

        if towards == ORDER_DIRECTION.BUY_CLOSE:
            # print("buyclose")
            # print(self.volume_short - self.volume_short_frozen)
            # print(amount)
            if (qapos.volume_short - qapos.volume_short_frozen) >= amount:
                # check
                qapos.volume_short_frozen_today += amount
                res = True
            else:
                print("BUYCLOSE 仓位不足")

        elif towards == ORDER_DIRECTION.BUY_CLOSETODAY:
            if (qapos.volume_short_today - qapos.volume_short_frozen_today) >= amount:
                qapos.volume_short_frozen_today += amount
                res = True
            else:
                print("BUYCLOSETODAY 今日仓位不足")
        elif towards == ORDER_DIRECTION.SELL_CLOSE:
            # print("sellclose")
            # print(self.volume_long - self.volume_long_frozen)
            # print(amount)
            if (qapos.volume_long - qapos.volume_long_frozen) >= amount:
                qapos.volume_long_frozen_today += amount
                res = True
            else:
                print("SELL CLOSE 仓位不足")

        elif towards == ORDER_DIRECTION.SELL_CLOSETODAY:
            if (qapos.volume_long_today - qapos.volume_short_frozen_today) >= amount:
                # print("sellclosetoday")
                # print(self.volume_long_today - self.volume_long_frozen)
                # print(amount)
                qapos.volume_long_frozen_today += amount
                return True
            else:
                print("SELLCLOSETODAY 今日仓位不足")
        elif towards in [ORDER_DIRECTION.BUY_OPEN,
                         ORDER_DIRECTION.SELL_OPEN,
                         ORDER_DIRECTION.BUY]:
            """
            冻结的保证金
            """
            coeff = float(price) * float(
                self.market_preset.get_code(code).get("unit_table",
                                                      1)
            ) * float(self.market_preset.get_code(code).get("buy_frozen_coeff",
                                                            1))
            moneyneed = coeff * amount
            if self.available > moneyneed:
                self.money -= moneyneed
                self.frozen[order_id] = {
                    'amount': amount,
                    'coeff': coeff,
                    'money': moneyneed
                }
                res = True
            else:
                self.log("开仓保证金不足 TOWARDS{} Need{} HAVE{}".format(
                    towards, moneyneed, self.available))

        return res

    def send_order(self, code: str, amount: float, price: float, towards: int, order_id: str = ''):
        order_id = str(uuid.uuid4()) if order_id == '' else order_id
        if self.order_check(code, amount, price, towards, order_id):
            # print("order check success")
            direction, offset = parse_orderdirection(towards)
            self.event_id += 1
            order = {
                "account_cookie": self.user_id,
                "user_id": self.user_id,
                "instrument_id": code,
                "towards": int(towards),
                "exchange_id": self.market_preset.get_exchange(code),
                "order_time": self.dtstr,
                "volume": float(amount),
                "price": float(price),
                "order_id": order_id,
                "seqno": self.event_id,
                "direction": direction,
                "offset": offset,
                "volume_orign": float(amount),
                "price_type": "LIMIT",
                "limit_price": float(price),
                "time_condition": "GFD",
                "volume_condition": "ANY",
                "insert_date_time": self.dtstr,
                "exchange_order_id": str(uuid.uuid4()),
                "status": 100,
                "volume_left": float(amount),
                "last_msg": "已报"
            }
            self.orders[order_id] = order
            return order
        else:
            print(RuntimeError("ORDER CHECK FALSE: {}".format(code)))
            return False
        self.sync()

    def cancel_order(self, order_id):
        """Initial
        撤单/ 释放冻结/

        """
        od = self.orders[order_id]
        od['last_msg'] = '已撤单'
        od['status'] = 500
        od['volume_left'] = 0
        frozen = self.frozen[order_id]

        self.money += frozen['money']

        frozen['amount'] = 0
        frozen['money'] = 0

        self.orders[order_id] = od
        self.frozen[order_id] = frozen

        self.log('撤单成功 {}'.format(order_id))

    def make_deal(self, order: dict):

        self.receive_deal(order["instrument_id"], trade_price=order["limit_price"], trade_time=self.dtstr,
                          trade_amount=order["volume_left"], trade_towards=order["towards"],
                          order_id=order['order_id'], trade_id=str(uuid.uuid4()))

    def receive_deal(self,
                     code,
                     trade_price,
                     trade_amount,
                     trade_towards,
                     trade_time,
                     message=None,
                     order_id=None,
                     trade_id=None,
                     realorder_id=None):
        if order_id in self.orders.keys():

            # update order
            od = self.orders[order_id]
            frozen = self.frozen[order_id]
            vl = od.get('volume_left', 0)
            if trade_amount == vl:

                self.money += frozen['money']
                frozen['amount'] = 0
                frozen['money'] = 0
                od['last_msg'] = '全部成交'
                od["status"] = 300
                self.log('全部成交 {}'.format(order_id))

            elif trade_amount < vl:
                frozen['amount'] = vl - trade_amount
                release_money = trade_amount * frozen['coeff']
                self.money += release_money

                frozen['money'] -= release_money

                od['last_msg'] = '部分成交'
                od["status"] = 200
                self.log('部分成交 {}'.format(order_id))

            od['volume_left'] -= trade_amount

            self.orders[order_id] = od
            self.frozen[order_id] = frozen
            # update trade
            self.event_id += 1
            trade_id = str(uuid.uuid4()) if trade_id is None else trade_id
            self.trades[trade_id] = {
                "seqno": self.event_id,
                "user_id":  self.user_id,
                "trade_id": trade_id,
                "exchange_id": od['exchange_id'],
                "instrument_id": od['instrument_id'],
                "order_id": order_id,
                "exchange_trade_id": trade_id,
                "direction": od['direction'],
                "offset": od['offset'],
                "volume": trade_amount,
                "price": trade_price,
                "trade_date_time": trade_time}

            # update accounts

            margin, close_profit = self.get_position(code).update_pos(
                trade_price, trade_amount, trade_towards)

            self.money -= margin
            self.close_profit += close_profit

            self.sync()

    def get_position(self, code: str = None) -> QA_Position:
        if code is None:
            return list(self.positions.values())[0]
        else:
            if code not in self.positions.keys():
                self.positions[code] = QA_Position(code=code)
            return self.positions[code]

    def query_trade(self):
        pass

    def on_tick(self, tick):
        pass

    def on_bar(self, bar):
        pass

    def on_price_change(self, code, price):

        try:
            pos = self.get_position(code)
            if pos.last_price == price:
                pass
            else:
                pos.last_price = price
                self.sync()
        except Exception as e:
            print(e)


if __name__ == "__main__":
    acc = QIFI_Account("x1", "x1")
    acc.initial()
    import pprint
    pprint.pprint(acc.message)

    r = acc.send_order('RB2001', 10, 5000, ORDER_DIRECTION.BUY_OPEN)
    print(r)

    acc.receive_deal(r['instrument_id'], 4500, r['volume'], r['towards'],
                     acc.dtstr, order_id=r['order_id'], trade_id=str(uuid.uuid4()))
    import pprint
    pprint.pprint(acc.message)

    acc.sync()

    acc2 = QIFI_Account("x1", "x1")
    acc2.initial()
    import pprint
    pprint.pprint(acc2.message)

    r = acc2.send_order('000001', 10, 12, ORDER_DIRECTION.BUY)
    print(r)

    acc2.receive_deal(r['instrument_id'], 11.8, r['volume'], r['towards'],
                      acc2.dtstr, order_id=r['order_id'], trade_id=str(uuid.uuid4()))
    import pprint
    pprint.pprint(acc2.message)

    acc2.sync()
