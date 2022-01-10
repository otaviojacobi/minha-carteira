from common.bovespa import Bovespa
from common.logger import Logger
from common.stock_response import StockNotFoundResponse, StockPriceResponse


def lambda_handler(event, _):

    logger = Logger('stock-price-now').instance()
    logger.debug(f'Received event: {event}')

    paper = event['pathParameters']['stock'].upper()

    try:
        b3 = Bovespa()
        price, paper = b3.get_current_stock_price(paper)
        logger.info(f'Stock {paper} found with price {price}')
        return StockPriceResponse(paper, price).json()
    except IndexError:
        logger.info(f'Stock {paper} not found')
        return StockNotFoundResponse(paper).json()
