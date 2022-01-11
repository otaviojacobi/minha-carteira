import uuid

import boto3
from common.crypt import encrypt
from common.exceptions import ResponseException
from common.logger import Logger
from dynamo_json import marshall, unmarshall

dynamodb = boto3.client('dynamodb')
unique_keys = ['username', 'email']
logger = Logger('user-crud').instance()

def __get_single_user_by_id(user_id, include_password=False):
    project_expression = 'id,email,username,password' if include_password else 'id,email,username'
    user = unmarshall(dynamodb.get_item(
            TableName='minha-carteira-user',
            Key=marshall({'id': user_id}),
            ProjectionExpression=project_expression
    )['Item'])
    if not all(key in set(user.keys()) for key in ['id', 'email', 'username']):
        raise Exception

    return user

def get_single_user(user_id):
    try:
        return __get_single_user_by_id(user_id)
    except Exception as e:
        logger.debug(f'Failed to get single user with exception {e}, user_id: {user_id}')
        raise ResponseException('User not found', 404)

def create_user(new_user):

    username = new_user['username']
    email = new_user['email']

    user_id = str(uuid.uuid4())

    encrypted_password = encrypt(new_user['password'])
    user = {
        'id': user_id,
        'username': username,
        'email': email,
        'password': encrypted_password
    }

    items = [{'id': f'{key}#{new_user[key]}'} for key in unique_keys]
    items.append(user)
    try:
        dynamodb.transact_write_items(TransactItems=[{
            'Put': {
                'TableName': 'minha-carteira-user',
                'ConditionExpression': 'attribute_not_exists(id)',
                'Item': marshall(item)
            }} for item in items])
    except dynamodb.exceptions.TransactionCanceledException as e:
        logger.debug(f'Create canceled {e}, user_id: {user_id}')
        raise ResponseException('User already exists')

    del user['password']

    return user

def update_user(user_id, update_info):

    prev_user = __get_single_user_by_id(user_id, include_password=True)
    if 'password' in update_info.keys():
        update_info['password'] = encrypt(update_info['password'])

    update_info = {k:v for k,v in update_info.items() if k in prev_user.keys()}

    # constraints
    delete_ids = [{'id': f'{key}#{prev_user[key]}'} for key in update_info.keys() 
        if prev_user[key] != update_info[key] and key in unique_keys]
    create_ids = [{'id': f'{key}#{update_info[key]}'} for key in update_info.keys() 
        if prev_user[key] != update_info[key] and key in unique_keys]

    delete_items = [{
        'Delete': {
            'TableName': 'minha-carteira-user',
            'ConditionExpression': 'attribute_exists(id)',
            'Key': marshall(item)
    }} for item in delete_ids]

    create_items = [{
        'Put': {
            'TableName': 'minha-carteira-user',
            'ConditionExpression': 'attribute_not_exists(id)',
            'Item': marshall(item)
    }} for item in create_ids]

    # update
    result_item = {**prev_user, **update_info}
    update_attribute_values = {f':{key}': value for key, value in result_item.items()}
    del update_attribute_values[':id']
    update_item = [{
        'Update': {
            'TableName': 'minha-carteira-user',
            'Key': marshall({'id': user_id}),
            'UpdateExpression': 'SET email = :email, username = :username, password = :password',
            'ExpressionAttributeValues': marshall(update_attribute_values)
        }
    }]
    dynamodb_items = delete_items+create_items+update_item

    del result_item['password']
    try:
        dynamodb.transact_write_items(TransactItems=dynamodb_items)
        return result_item
    except Exception as e:
        logger.debug(f'Update canceled {e}, user_id: {user_id}')
        logger.debug(f'Update transaction items {dynamodb_items}')
        raise ResponseException('Could not update user', 400)


def delete_user(user_id):

    try:
        user = __get_single_user_by_id(user_id)
        items = [{'id': f'username#{user["username"]}'}, {'id': f'email#{user["email"]}'}, {'id': user_id}]
        dynamodb.transact_write_items(TransactItems=[{
            'Delete': {
                'TableName': 'minha-carteira-user',
                'ConditionExpression': 'attribute_exists(id)',
                'Key': marshall(item)
            }} for item in items])
    except Exception as e:
        logger.debug(f'Delete canceled {e}, user_id: {user_id}')
        raise ResponseException('User not found', 404)
