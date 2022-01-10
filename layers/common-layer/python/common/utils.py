import json

from common.exceptions import ResponseException


# Decorators
def capture_value_error(fn):
    def inner(event, context):
        try:
            return fn(event, context)
        except ResponseException as e:
            return {
                'statusCode': e.status_code,
                'body': json.dumps({'message': e.message})
            }
    return inner
