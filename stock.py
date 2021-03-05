#import matplotlib.pyplot as plt
from urllib.request import urlopen
import robin_stocks.robinhood as rh
import pyotp
import json

class stock:
    def __init__(self, file):
        with open(file, 'r') as f:
            info = f.read().splitlines()
        totp  = pyotp.TOTP(info[0]).now()
        rh.login(info[1], info[2], mfa_code = totp)
        self.positions = {}
        for position in rh.get_open_stock_positions():
            with urlopen(position['instrument']) as response:
                instr = json.loads(response.read())
            content = {
                    'name': instr['simple_name'],
                    'shares': float(position['quantity'])
                    }
            self.positions.update({instr['symbol']: content})

    def __repr__(self):
        content = ""
        for symbol in self.positions:
            content += f"{symbol}: {self.positions[symbol]}\n"
        return content

    def symbol(self):
        return [symbol for symbol in self.positions]

    def equity(self):
        positions = rh.account.build_holdings()
        return [(symbol, float(positions[symbol]['quantity'])) for symbol in self.positions if float(positions[symbol]['equity_change']) < 5 ]

    def watchlist(self):
        return [stock['symbol'] for stock in rh.account.get_watchlist_by_name(info='results') if not stock['symbol'] in self.positions]

    def sell(self, symbol):
        quantity = self.positions.pop(symbol)['quantity']
        return rh.orders.order_sell_fractional_by_quantity(symbol, quantity)

    def buy(self, symbol):
        info = rh.orders.order_buy_fractional_by_price(symbol, MONEY)
        self.positions.update({symbol: {'name': None, 'shares': None}})
        return info

    def cash(self):
        return float(rh.profiles.load_account_profile('buying_power'))

    def history(self, symbol):
        return rh.stocks.get_stock_historicals(symbol, '5minute', 'week', info='close_price')

    def SMA(self, prices):
        total = 0
        for price in prices:
            total += float(price)
        return total / len(prices)

    def EMA(self, prices):
        ema = self.SMA(prices[0:10])
        c = 2 / (1 + len(prices[10:-1]))
        for price in prices[10:-1]:
            ema = float(price) * c + ema * (1 - c)
        return ema
