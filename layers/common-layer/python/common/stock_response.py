import json
from datetime import datetime as dt


class Response:

    def __init__(self, status_code, body):
        self.status_code = status_code
        self.body = body

    def json(self):
        return {
            'statusCode': self.status_code,
            'body': json.dumps(self.body)
        }


class StockNotFoundResponse(Response):
    def __init__(self, paper):
        super().__init__(400, {'message': f'Paper {paper} not found.'})


class StockPriceResponse(Response):
    def __init__(self, paper, price):
        super().__init__(200, {'stock': paper, 'price': price, 'timestamp': dt.now().isoformat()})

class MultipleStockPriceResponse(Response):
    def __init__(self, stock_prices):
        time_stamp = dt.now().isoformat()
        stock_prices = [{'stock': paper, 'price': price, 'timestamp': time_stamp} for price, paper in stock_prices]
        super().__init__(200, stock_prices)

class TooManyStocksResponse(Response):
    def __init__(self):
        super().__init__(400, {'message': 'Please request less than 100 papers at a time.'})
