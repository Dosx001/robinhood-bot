import robin_stocks.robinhood as rh
import pyotp

with open('/home/dosx/.tokens/info.txt', 'r') as f:
    info = f.read().splitlines()

totp  = pyotp.TOTP(info[0]).now()
login = rh.login(info[1], info[2], mfa_code = totp)

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
