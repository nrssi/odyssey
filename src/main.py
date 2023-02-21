from blockchain import BlockChain, Block
if __name__ == "__main__":
    bc = BlockChain()
    bc.add_block(Block(bc.get_length(), {}, ""))
    bc.add_block(Block(bc.get_length(), {"enter":"the dragon"},bc.get_latest_block().hash))
    bc.serialize()
    print(bc)
