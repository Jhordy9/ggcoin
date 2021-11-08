import hashlib
import json


class Hash:
    def generate_hash(block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def int_hash(hash):
        return int(hash, 16)
