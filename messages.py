import json
import hashlib
from cryptography.fernet import Fernet
import time

class Block:
    def __init__(self, data, block_hash, previous_hash, difficulty, timestamp=time.time_ns()):
        self.data = data
        self.block_hash = block_hash
        self.previous_hash = previous_hash
        self.difficulty = difficulty
        self.timestamp = timestamp
        
    def __repr__(self):
        return json.dumps(self.__dict__)
    
    def genesis():
        key = Fernet.generate_key()
        return Block(key.decode(), "genesis hash", "0x0", 1)
    
    def mine_block(last_block, message="", key=Fernet.generate_key()):
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(message.encode('utf-8'))
        timestamp = time.time_ns()
        last_hash = last_block.block_hash
        difficulty = last_block.difficulty
        nonce = 0
        
        while True:
            hash_input = f"{timestamp}{last_hash}{encrypted_data}{nonce}".encode('utf-8')
            hash_value = hashlib.sha256(hash_input).hexdigest()
            print(hash_value)
            
            if hash_value.startswith('a' * difficulty):
                new_block = Block(
                    data=encrypted_data,
                    block_hash=hash_value,
                    previous_hash=last_hash,
                    difficulty=difficulty,
                    timestamp=timestamp
                )
                return new_block
            nonce += 1


# The first block in the chain holds the key here
def send_message(chain, message):
    key = chain[0].data.encode()
    new_block = Block.mine_block(chain[-1], message, key)
    chain.append(new_block)
    print(f"\n✅ Message minded into block: {new_block.block_hash[:20]}... ⛏️ ⛏️ ⛏️\n")
    return new_block

def decrypt_message(block, genesis_block):
    try:
        key = genesis_block.data.encode()
        fernet = Fernet(key)
        return fernet.decrypt(block.data).decode('utf-8')
    except:
        return "⚠️  Busted chain or wrong key!"
    
if __name__ == '__main__':
    genesis = Block.genesis()  # Key vault born!
    print(f"🗝️ Genesis (key holder): {genesis}\n")
    
    chain = [genesis]
    messages = ["Calantib: 'Meet at high noon'", "Numerius: 'Gold in the river'"]
    
    # Mine 'em in...
    cal_block = send_message(chain, messages[0])
    num_block = send_message(chain, messages[1])
    
    # DECRYPT SHOWDOWN! 🔓
    print("\n🔍 Decryption Report:")
    print(f"Calantib's whisper: '{decrypt_message(cal_block, genesis)}'")
    print(f"Numerius's secret: '{decrypt_message(num_block, genesis)}'")
    
    # Tamper test: Mess with a block → decryption fails!
    cal_block.data = b"TAMPERED!!"  
    print(f"Tampered Calantib: '{decrypt_message(cal_block, genesis)}'\n")
    
    print("💡 Full chain:")
    for i, block in enumerate(chain):
        msg = decrypt_message(block, genesis) if i > 0 else "🔑 [KEY]"
        print(f"Block {i}: {block.block_hash[:12]}...\t ➡️   {msg}")