import json

from common.bovespa import Bovespa
from common.logger import Logger
from common.stock_response import (MultipleStockPriceResponse,
                                   TooManyStocksResponse)


def lambda_handler(event, _):

    logger = Logger('stock-price').instance()
    logger.debug(f'Received event: {event}')

    request_stocks = json.loads(event['body'])
    logger.info(f'Will predict stocks {request_stocks}')


    if len(request_stocks) > 100:
        return TooManyStocksResponse()

    b3 = Bovespa()
    if len(request_stocks) == 0:
        stocks_price = []
    elif len(request_stocks) == 1:
        stocks_price = [b3.get_current_stock_price(request_stocks[0])]
    else:
        stocks_price = b3.get_current_multiple_stock_prices(request_stocks)

    logger.info(stocks_price)

    return MultipleStockPriceResponse(stocks_price).json()
