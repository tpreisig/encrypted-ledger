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
        self.nonce = nonce  

    def __repr__(self):
        # Convert bytes data to base64 string for repr
        dict_copy = self.__dict__.copy()
        if isinstance(self.data, bytes):
            dict_copy['data'] = base64.urlsafe_b64encode(self.data).decode('utf-8')
        return json.dumps(dict_copy, indent=4)
    
    @classmethod
    def genesis(cls):
        key = Fernet.generate_key()
        return cls(key.decode(), "genesis", "0000")

    @classmethod
    def mine_block(cls, last_block, message="muh", key=Fernet.generate_key()):
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(message.encode('utf-8'))
        timestamp = time.time_ns()
        last_hash = last_block.block_hash
        difficulty = last_block.difficulty  # Could also be adaptive: +1 if conditions met
        nonce = 0
        while True:
            encrypted_data_str = base64.urlsafe_b64encode(encrypted_data).decode('utf-8')
            hash_input = f"{timestamp}{last_hash}{encrypted_data_str}{nonce}".encode('utf-8')
            hash_value = hashlib.sha256(hash_input).hexdigest()
            print(f"0x{hash_value}")

            if hash_value.startswith('0' * difficulty):
                new_block = cls(
                    data=encrypted_data,
                    block_hash=hash_value,
                    last_hash=last_hash,
                    difficulty=difficulty,
                    timestamp=timestamp,
                    nonce=nonce  # Store the nonce
                )
                return new_block
            nonce += 1
      
    
    def validate(self, previous_block):
        if self.last_hash != previous_block.block_hash:
            return False
        # Recompute hash to verify integrity (handle bytes or str data)
        if isinstance(self.data, bytes):
            data_str = base64.urlsafe_b64encode(self.data).decode('utf-8')
        else:
            data_str = self.data
        recomputed_input = f"{self.timestamp}{self.last_hash}{data_str}{self.nonce}".encode('utf-8')
        recomputed_hash = hashlib.sha256(recomputed_input).hexdigest()
        return self.block_hash == recomputed_hash

def validate_chain(chain):
    for i in range(1, len(chain)):
        current = chain[i]
        previous = chain[i-1]
        if not current.validate(previous):
            return False
    return True

def send_message(chain, message):
    key = chain[0].data.encode()  # Genesis key needs to be encoded
    new_block = Block.mine_block(chain[-1], message, key)
    chain.append(new_block)
    print(f"\n✅ Message mined into block: 0x{new_block.block_hash[:20]}... ⛏️ ⛏️ ⛏️\n")  

def read_chain(chain):
    if not validate_chain(chain):
        print("Chain tampered! Aborting.")
        return
    key = chain[0].data.encode()  # Need to encode the key string
    fernet = Fernet(key)

    for block in chain[1:]:  # Skip genesis
        decrypted = fernet.decrypt(block.data).decode()
        print(f"🔑 Block 0x{block.block_hash[:20]}... (Nonce: {block.nonce}): {decrypted}")

if __name__ == "__main__":
    chain = [Block.genesis()]
    messages = ["Secret message 932", "Hidden intel 9", "Covert plan 3"]

    for msg in messages:
        send_message(chain, msg)

    print("\nDecoding the blockchain messages:\n")
    read_chain(chain)