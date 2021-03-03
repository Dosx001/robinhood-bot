import matplotlib.pyplot as plt
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
                    'shares': position['quantity']
                    }
            self.positions.update({instr['symbol']: content})

    def __repr__(self):
        content = ""
        for position in self.positions:
            content += f"{position}: {self.positions[position]}\n"
        return content

    def SMA(self, prices):
        total = 0
        for price in prices:
            total += price
        return total / len(prices)

    def EMA(self, prices):
        ema = SMA(prices[0:10])
        c = 2 / (1 + len(prices[10:-1]))
        for price in prices[10:-1]:
            ema = price * c + ema * (1 - c)
        return ema
