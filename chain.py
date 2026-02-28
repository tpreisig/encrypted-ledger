import json
import os
from random import randint

def imposter_hash(data):
    # function that generates a simulated random 256-bit hash value, 
    # just for the sake of it, even though it's way easier to import a real hash function from hashlib 😅
    return f"0x{randint(0, 1<<256):064x}"

class Block:
    def __init__(self, data, previous_hash=None):
        self.data = data
        self.previous_hash = previous_hash
        self.hash = imposter_hash(f"{data}{previous_hash}")

    def __repr__(self):
        return f"Block(data={self.data}, previous_hash={self.previous_hash}, hash={self.hash})"


class Blockchain:
    def __init__(self):
        genesis_block = Block(data="Genesis Block", previous_hash="0x0")
        self.blocks = [genesis_block] # initialize the blockchain with the genesis block
        
    def add_block(self, data):
        last_block = self.blocks[-1]
        new_block = Block(data=data, previous_hash=last_block.hash)
        self.blocks.append(new_block) # add the new block to the blockchain
