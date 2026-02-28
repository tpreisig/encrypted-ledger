import json
import os
from random import randint

def imposter_hash(data):
    # function that generates a simulated random 256-bit hash value, 
    # just for the sake of it, even though it's way easier to import a real hash function from hashlib 😅
    return f"0x{randint(0, 1<<256):064x}"

