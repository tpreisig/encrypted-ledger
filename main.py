import json
import hashlib
from cryptography.fernet import Fernet
import time
import base64

class Block:
    def __init__(self, data, block_hash, last_hash, difficulty=1, timestamp=None, nonce=0):
        self.data = data
        self.block_hash = block_hash
        self.last_hash = last_hash
        self.difficulty = difficulty
        self.timestamp = timestamp
        self.nonce = nonce  # Added to store nonce for validation

    def __repr__(self):
        # Fix for JSON serialization: Convert bytes data to base64 string for repr
        dict_copy = self.__dict__.copy()
        if isinstance(self.data, bytes):
            dict_copy['data'] = base64.urlsafe_b64encode(self.data).decode('utf-8')
        return json.dumps(dict_copy, indent=4)

   @classmethod
    def genesis(cls):
        key = Fernet.generate_key()
        return cls(key.decode(), "genesis", "0000")

    @classmethod
    def mine_block(cls, last_block, message="Muh", key=Fernet.generate_key()):
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(message.encode('utf-8'))
        timestamp = time.time_ns()
        last_hash = last_block.block_hash
        difficulty = last_block.difficulty  # Could add adaptive: +1 if conditions met, but keeping simple
        nonce = 0
