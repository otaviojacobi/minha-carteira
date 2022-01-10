import uuid

import boto3
from common.crypt import encrypt
from dynamo_json import marshall

dynamodb = boto3.client('dynamodb')

def get_all_users():
    pass

def get_single_user(user_id):
    pass

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

    items = [{'id': f'username#{username}'}, {'id': f'email#{email}'}, user]

    try:
        dynamodb.transact_write_items(TransactItems=[{
            'Put': {
            'TableName': 'minha-carteira-user', 
            'ConditionExpression': 'attribute_not_exists(id)',
            'Item': marshall(item) }
        } for item in items])
    except dynamodb.exceptions.TransactionCanceledException:
        raise ValueError('User already exists')

    del user['password']

    return user

def update_user(user_id, update_info):
    pass

def delete_user(user_id):
    pass
