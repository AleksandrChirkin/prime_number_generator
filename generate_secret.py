import uuid


with open('secret_key.txt', mode='w') as secret:
    secret.write(str(uuid.uuid4()))
