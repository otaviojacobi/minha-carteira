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
        if event['resource'] == '/user':
            return user_crud.get_all_users()
        return user_crud.get_single_user(event['pathParameters']['id'])

    if http_method == 'POST':
        user = user_crud.create_user(json.loads(event['body']))
        return {
            'statusCode': 201,
            'body': json.dumps(user)
        }

    if http_method == 'PUT':
        return user_crud.update_user(event['pathParameters']['id'], json.loads(event['body']))

    if http_method == 'DELETE':
        return user_crud.delete_user(event['pathParameters']['id'])
