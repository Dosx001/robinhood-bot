from stock import stock

def main():
    robin = stock('/home/dosx/.tokens/info.txt')
    for symbol in robin.watchlist():
        print(symbol)
        prices = robin.history(symbol)
        print(f"SMA: {robin.SMA(prices)}")
        print(f"EMA: {robin.EMA(prices)}")

if __name__ == '__main__':
    main()
