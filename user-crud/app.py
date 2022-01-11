import json

from common.logger import Logger
from common.utils import capture_value_error

import user_crud


@capture_value_error
def lambda_handler(event, _):

    logger = Logger('user-crud').instance()
    logger.debug(f'Received event: {event}')

    http_method = event['httpMethod']

    if http_method == 'GET':
        user = user_crud.get_single_user(event['pathParameters']['id'])
        return {
            'statusCode': 200,
            'body': json.dumps(user)
        }

    if http_method == 'POST':
        user = user_crud.create_user(json.loads(event['body']))
        return {
            'statusCode': 201,
            'body': json.dumps(user)
        }

    if http_method == 'PUT':
        user = user_crud.update_user(event['pathParameters']['id'], json.loads(event['body']))
        return {
            'statusCode': 200,
            'body': json.dumps(user)
        }


    if http_method == 'DELETE':
        user_crud.delete_user(event['pathParameters']['id'])
        return {
            'statusCode': 204
        }

    return {
        'statusCode': 400,
        'messsage': 'Invalid request'
    }
