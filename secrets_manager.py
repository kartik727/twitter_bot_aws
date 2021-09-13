import boto3
import os

from base64 import b64decode

class SecretsManager:
    def __init__(self):
        self.decrypted = {}
        
    def __call__(self, key):
        if key in self.decrypted:
            return self.decrypted[key]
        else:
            dec = self.decrypt(key)
            self.decrypted[key] = dec
            return dec
            
    def decrypt(self, key):
        enc = os.environ[key]
        dec = boto3.client('kms').decrypt(
            CiphertextBlob=b64decode(enc),
            EncryptionContext={'LambdaFunctionName': os.environ['AWS_LAMBDA_FUNCTION_NAME']}
            )['Plaintext'].decode('utf-8')
        return dec
