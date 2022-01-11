import json

import numpy as np
import pandas as pd

from common.exceptions import ResponseException
from common.logger import Logger

logger = Logger('utils').instance()
# Decorators
def capture_value_error(fn):
    def inner(event, context):
        try:
            return fn(event, context)
        except ResponseException as e:
            logger.debug(f'ResponseException {e}')
            return {
                'statusCode': e.status_code,
                'body': json.dumps({'message': e.message})
            }
    return inner
