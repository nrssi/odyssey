"""
This module contains all the definitions and declarations required for a fully functional Blockchain implementation
this will also include serialization and deserialization methods for Blockchain to store and load data files.
"""
import hashlib
import datetime
import os
from json import load as load_json, dumps as dump_json
from typing import Dict

class BlockInsertionError(Exception):
    """
    This error is raised when there's a problem inserting a block into the blockchain
    mostly when the data inside is corrupt
    """
    def __init__(self, message : str | None) -> None:
        self.msg = message

BLOCKCHAIN_STORE = "store.json"
"""This variable contains the filename used when storing the blockchain to storage, same will be used while reinitializing"""
class Block:
    """
    ### Class Block
    This class is the representation of a node in blockchain 
    it contains, 
    - index : specifies the place of the block in blockchain
    - timestamp : specifies the time period at w3hich block is created
    - data : contains actual data (i,e polling info in current context)
    - previous_hash : contains a hash computed from the previous block
    - hash : contains hash value for the current block
    """
    def __init__(self, index:int, data:Dict[str, str], previous_hash:str) -> None:
        """
        Params:
           - index : represents the position of block in blockchain
           - data : A dictionary that contains voter ID as key and candidate ID as value
           - previous_hash : hash value of previous block in blockchain (for maintaining integritty in data)
           ---
        Returns: **None**
        """
        self.index = index
        self.timestamp = f"{datetime.datetime.now()}"
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        """
        Params :
           - None  
           ----
        Returns : **string representing a hash of the entire block**  

        ---
        This function is used to calculate a hash value. Hash value is generated using all the data in the block, this hash contains the hash of previous node's hash too.
        **Hash256** algorightm is used to generate this hash value.
        """
        sha = hashlib.sha256()
        sha.update(str(self.index).encode('utf-8') +
                   str(self.timestamp).encode('utf-8') +
                   str(self.data).encode('utf-8') +
                   str(self.previous_hash).encode('utf-8'))
        return sha.hexdigest()

    def __repr__(self) -> str:
        return f"{self.__dict__}" 

    def dict(self) -> Dict:
        """This function returns a dictionary containing all the values in block, this function is used as helper in serializing block to json format"""
        return self.__dict__

class BlockChain:
    """
    ### Class BlockChain
    This class is going to be the main blockchain implementation 
    it's going to contain a list of nodes(Blocks in current context) and some additional 
    error correction data
    """
    def __init__(self) -> None:
        if os.path.exists(BLOCKCHAIN_STORE):
            self.chain = load_json(open(BLOCKCHAIN_STORE))
        else:
            with open(BLOCKCHAIN_STORE, 'w'):
                pass
        self.chain = [Block(0, {"ID":"Intial Block"}, "")]

    def get_length(self) -> int:
        return len(self.chain)
    # returns the last block of the chain (which is probably the most recent insertion)
    def get_latest_block(self) -> Block:
        return self.chain[-1]
    
    # adds block to the blockchain 
    def add_block(self, new_block : Block) -> bool:
        if self.is_valid() : 
            new_block.previous_hash = self.get_latest_block().hash
            new_block.hash = new_block.calculate_hash()
            self.chain.append(new_block)
            return True
        else:
            return False

   # returns true or false based on the state of blockchain
   # True if unaltered and not corrupted
   # False if altered or corrupted
    def is_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True
    def serialize(self) -> None:
        json_data = dump_json(self, default=lambda o: o.__dict__, indent=4)
        with open(BLOCKCHAIN_STORE, 'w') as f:
            f.write(json_data)
    # use this for DEBUG only
    def __repr__(self) -> str:
        return f"{self.__dict__}"
