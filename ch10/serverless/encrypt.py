import boto3
import base64

import sys
import os

if __name__ == '__main__':
    key_id = os.environ["KEY_ARN"]
    client = boto3.client('kms')

    stuff = client.encrypt(KeyId=key_id, Plaintext='supersecret')

    binary_encrypted = stuff[u'CiphertextBlob']
    print(binary_encrypted)
    encrypted_password = base64.b64encode(binary_encrypted)
    print(encrypted_password.decode())
    #print(base64.b64decode('binary_encrypted'))

    print(client.decrypt(CiphertextBlob=binary_encrypted))
