import matplotlib.pyplot as plt
from urllib.request import urlopen
import robin_stocks.robinhood as rh
import pyotp
import json

with open('/home/dosx/.tokens/info.txt', 'r') as f:
    info = f.read().splitlines()

totp  = pyotp.TOTP(info[0]).now()
login = rh.login(info[1], info[2], mfa_code = totp)

def main():
    for stock in rh.get_open_stock_positions():
        with urlopen(stock['instrument']) as response:
            instr = json.loads(response.read())
        prices = rh.stocks.get_stock_historicals(instr['symbol'], '5minute', 'week', info = 'close_price')
        x = []
        for index, price in enumerate(prices):
            prices[index] = float(price)
            x.append(index)
        plt.figure(instr['name'])
        plt.plot(x, prices)
        plt.grid()
    plt.show()

def SMA(prices):
    total = 0
    for price in prices:
        total += price
    return total / len(price)

def EMA(prices):
    ema = SMA(prices[0:10])
    c = 2 / (1 + len(prices[10:-1]))
    for price in prices[10:-1]:
        ema = price * c + ema * (1 - c)
    return ema

if __name__ == '__main__':
    main()
