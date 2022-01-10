import math

import yfinance as yf


class Bovespa:

    def __init__(self):
        pass

    def get_current_stock_price(self, paper):
        close_history = yf.Ticker(f'{paper}.SA').history(period='2d').tail(1)['Close']
        return close_history.iloc[0], paper

    def get_current_multiple_stock_prices(self, papers):
        tickers = yf.Tickers('.SA '.join(papers) + '.SA')
        close_history = tickers.history(period='2d').tail(1)['Close']

        price_papers = []
        for paper in papers:
            price = close_history[f'{paper}.SA'].iloc[0]
            if not math.isnan(price):
                price_papers.append((price, paper))


        return price_papers
