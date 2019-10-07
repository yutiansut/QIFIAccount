import datetime
import uuid
from QUANTAXIS.QAARP.market_preset import MARKET_PRESET
from QUANTAXIS.QAMarket.QAPosition import QA_Position


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


class QIFI_Account():

    def __init__(self, username, password, model="SIM", broker_name="QUANTAXIS"):
        """Initial
        QIFI Account是一个基于 DIFF/ QIFI/ QAAccount后的一个实盘适用的Account基类


        1. 兼容多持仓组合
        2. 动态计算权益

        使用 model = SIM/ REAL来切换


        """
        self.user_id = ""
        self.username = ""
        self.password = ""

        self.source_id = "QIFI_Account"  # 识别号
        self.market_preset = MARKET_PRESET()
        # 指的是 Account所属的账户编组(实时的时候的账户观察组)
        self.portfolio = ""
        self.model = model

        self.broker_name = broker_name    # 所属期货公司/ 模拟的组
        self.investor_name = ""  # 账户所属人(实盘的开户人姓名)
        self.bank_password = ""
        self.capital_password = ""
        self.wsuri = ""

        self.bank_id = "QASIM"
        self.bankname = "QASIMBank"

        self.pub_host = ""
        self.trade_host = ""
        self.last_updatetime = ""
        self.status = 200
        self.trading_day = ""

        self.pre_balance = 0
        self._balance = 0
        self.static_balance = 0

        self.deposit = 0  # 入金
        self.withdraw = 0  # 出金
        self.withdrawQuota = 0  # 可取金额
        self.close_profit = 0
        self.event_id = 0

        # QIFI 协议
        self.transfers = {}

        self.banks = {}

        self.events = {}
        self.positions = {}
        self.trades = {}
        self.orders = {}

    def initial(self):
        try:
            self.reload()
        except:
            pass

        if self.pre_balance == 0 and self._balance == 0 and self.model == "SIM":
            self.create_simaccount()

        self.sync()

    def reload(self):
        pass

    def sync(self):
        pass

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

    @property
    def message(self):
        return {
            # // 账户号(兼容QUANTAXIS QAAccount)// 实盘的时候是 账户id
            "account_cookie": self.user_id,
            "password": self.password,
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
            "trading_day": self.trading_day,
            "status": self.status,
            "accounts": self.account_msg,
            "trades": self.trade_msg,
            "positions": self.position_msg,
            "orders": self.order_msg,
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
            "frozen_margin": 0.0,
            "frozen_commission": 0.0,
            "frozen_premium": 0.0,
            "available": self.available,
            "risk_ratio": 0.0
        }

    @property
    def order_msg(self):
        """struct to json

        Returns:
            [type] -- [description]
        """

        return dict(zip(self.orders.keys(), [item.to_dict() for item in self.orders]))

    @property
    def trade_msg(self):
        """struct to json

        Returns:
            [type] -- [description]
        """

        return {

        }

    @property
    def position_msg(self):
        return {

        }

    @property
    def position_profit(self):
        pass

    @property
    def float_profit(self):
        pass

# 惰性计算
    @property
    def available(self):
        return 0

    @property
    def margin(self):
        """保证金
        """
        pass

    @property
    def commission(self):
        pass

    @property
    def premium(self):
        pass

    @property
    def balance(self):
        """动态权益

        Arguments:
            self {[type]} -- [description]
        """

        return self._balance

    def order_check(self, code: str, amount: float, price: float, towards: int, order_id: str) -> bool:
        res = False
        qapos = self.get_position(code)

        if towards == ORDER_DIRECTION.BUY_CLOSE:
            # print("buyclose")
            #print(self.volume_short - self.volume_short_frozen)
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
            #print(self.volume_long - self.volume_long_frozen)
            # print(amount)
            if (qapos.volume_long - qapos.volume_long_frozen) >= amount:
                qapos.volume_long_frozen_today += amount
                res = True
            else:
                print("SELL CLOSE 仓位不足")

        elif towards == ORDER_DIRECTION.SELL_CLOSETODAY:
            if (qapos.volume_long_today - qapos.volume_short_frozen_today) >= amount:
                # print("sellclosetoday")
                #print(self.volume_long_today - self.volume_long_frozen)
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
            moneyneed = float(amount) * float(price) * float(
                self.market_preset.get_code(code).get("unit_table",
                                       1)
            ) * float(self.market_preset.get_code(code).get("buy_frozen_coeff",
                                             1))

            if self.available > moneyneed:
                self.available -= moneyneed
                #self.frozen
                #[order_id] = moneyneed
                res = True
            else:
                print("开仓保证金不足 TOWARDS{} Need{} HAVE{}".format(
                    towards, moneyneed, self.available))

        return res

    def send_order(self, code: str, amount: float, price: float, towards: int):
        order_id = str(uuid.uuid4())
        if self.order_check(code, amount, price, towards, order_id):
            #print("order check success")
            order = {
                "account_cookie": self.user_id,
                "instrument_id": code,
                "towards": int(towards),
                "exchange_id": self.market_preset.get_exchange(code),
                "order_time": self.dtstr,
                "volume": float(amount),
                "price": float(price),
                "order_id": order_id,
                "status": 100
            }
            self.orders[order_id] = order
            return order
        else:
            print(RuntimeError("ORDER CHECK FALSE: {}".format(code)))
            return False

    def receive_deal(self, ):
        pass

    def get_position(self, code=None):
        if code is None:
            return list(self.positions.values())[0]
        else:
            if code not in self.positions.keys():
                self.positions[code] = QA_Position(code=code)
            return self.positions[code]

    def query_trade(self):
        pass


if __name__ == "__main__":
    acc = QIFI_Account("x1", "x1")
    acc.initial()
    import pprint
    pprint.pprint(acc.message)