from cryptography.hazmat.primitives.serialization import load_pem_private_key

def load_secret_key(secret_key: str):
    return bytes(secret_key, 'latin-1')

def load_private_key(private_key_path):
    with open(private_key_path, 'rb') as f:
        private_key = load_pem_private_key(data=f.read(), password=None)
    return private_key