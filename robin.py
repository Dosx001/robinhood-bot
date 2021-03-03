from stock import stock

def main():
    robin = stock('/home/dosx/.tokens/info.txt')
    robin.watchlist()

if __name__ == '__main__':
    main()
