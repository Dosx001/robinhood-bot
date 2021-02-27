import robin_stocks.robinhood as rh
import pyotp

with open('/home/dosx/.tokens/info.txt', 'r') as f:
    info = f.read().splitlines()

totp  = pyotp.TOTP(info[0]).now()
login = rh.login(info[1], info[2], mfa_code = totp)
