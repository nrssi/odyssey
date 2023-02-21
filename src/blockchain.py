import hashlib
import datetime
from typing import Dict

class Block:
    '''
    This class is the basic representation of what each node in our blockchain is going to be 
    it's going to contain every piece of information required for operation 
    '''
    def __init__(self, index:int, data:Dict, previous_hash:str) -> None:
        self.index = index
        self.timestamp = datetime.datetime.now()
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    # returns a hash that will be used for error checking
    def calculate_hash(self) -> str:
        sha = hashlib.sha256()
        sha.update(str(self.index).encode('utf-8') +
                   str(self.timestamp).encode('utf-8') +
                   str(self.data).encode('utf-8') +
                   str(self.previous_hash).encode('utf-8'))
        return sha.hexdigest()

    # use this for DEBUG only 
    def print_block(self) -> None:
        print(self.__dict__)


class Blockchain:
    '''
    This class is going to be the main blockchain implementation 
    it's going to contain a list of nodes(Blocks in current context) and some additional 
    error correction data
    '''
    def __init__(self) -> None:
        self.chain = [self.create_initial_block()]

    # creates initial block of the blockchain with default parameters 
    # TODO : fix this to create a chain based on the given arguments
    def create_initial_block(self) -> Block:
        return Block(0, {"message" : "Genesis Block"}, "0")
    
    # returns the last block of the chain (which is probably the most recent insertion)
    def get_latest_block(self) -> Block:
        return self.chain[-1]
    
    # adds block to the blockchain 
    # TODO : perform error checking to make sure blockchain is not in altered state
    # fail the insertion of it's not valid 
    def add_block(self, new_block) -> None:
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

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

    # use this for DEBUG only
    def print_chain(self) -> None:
        print(self.__dict__)
