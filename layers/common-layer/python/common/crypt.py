from base64 import b64encode

import boto3


def encrypt(value):
    kms = boto3.client('kms')

    encoded_encrypted_password = kms.encrypt(
        KeyId='alias/minha-carteira-key',
        Plaintext=value
    )['CiphertextBlob']

    return b64encode(encoded_encrypted_password).decode('ascii')
