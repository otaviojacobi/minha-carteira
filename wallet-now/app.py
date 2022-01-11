import json

from common.logger import Logger
from common.wallet import Wallet


def lambda_handler(event, _):

    logger = Logger('wallet-now').instance()
    logger.debug(f'Received event: {event}')

    request_stocks = json.loads(event['body'])
    logger.info(f'Will predict wallet {request_stocks}')

    wallet = Wallet(request_stocks)

    return {
        'statusCode': 200,
        'value': wallet.value()
    }
