import time
import hashlib
import json
from uuid import uuid4


class Blockchain:
    def __init__(self, current_node_url=None):
        self.chain = []
        self.pending_transactions = []
        self.current_node_url = current_node_url
        
        self.network_nodes = []
        self.create_new_block(100,'0','0')

    def create_new_block(self, nonce, previous_block_hash, hash_):
        new_block = {
            'index': len(self.chain) + 1,
            'timestamp': int(time.time() * 1000),
            'transactions': self.pending_transactions,
            'nonce': nonce,
            'hash': hash_,
            'previous_block_hash': previous_block_hash,
        }
        self.pending_transactions = []
        self.chain.append(new_block)
        return new_block
    
    def get_last_block(self):
        return self.chain[len(self.chain) - 1]
    
    def create_new_transaction(self,amount,sender,recipient):
        new_transaction = {
            'amount' : amount,
            'sender' : sender,
            'recipient' : recipient,
            'transaction_id': str(uuid4()).replace('-', '')
        }
        return new_transaction

    def hash_block(self, previous_block_hash, current_block_data, nonce):
        data_as_string = previous_block_hash + str(nonce) + json.dumps(current_block_data, separators=(',', ':'))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
        hash_object = hashlib.sha256(data_as_string.encode())
        hash_ = hash_object.hexdigest()
        return hash_
    
    def proof_of_work(self,previous_block_hash, current_block_data):
        nonce = 0
        hash_ = self.hash_block(previous_block_hash, current_block_data, nonce)
        while hash_[:4] != '0000':
            nonce += 1
            hash_ = self.hash_block(previous_block_hash, current_block_data, nonce)
            print(hash_)
        return nonce
    
    def add_transaction_to_pending_transactions(self,transaction_obj):
        self.pending_transactions.append(transaction_obj)
        return self.get_last_block()['index'] + 1
    

    def chain_is_valid(self, chain):
        genesis_block = chain[0]
        correct_nonce = genesis_block['nonce'] == 100
        correct_previous_block_hash = genesis_block['previous_blockHash'] == '0'
        correct_hash = genesis_block['hash'] == '0'
        correct_transactions = len(genesis_block['transactions']) == 0
        validChain  = True

        if not (correct_nonce and correct_previous_block_hash and correct_hash and correct_transactions):
            print("1")
            validChain = False

        for i in range(1, len(chain)):
            current_block = chain[i]
            prev_block = chain[i - 1]

            block_hash = self.hash_block(prev_block['hash'],{"transactions": current_block['transactions'], "index": current_block['index']}, current_block['nonce'])
            print(block_hash)
            if block_hash[:4] != '0000':
                validChain = False

            if current_block['previousBlockHash'] != prev_block['hash']:
                validChain = False

        return validChain
    
    def get_block(self, block_hash):
        correct_block = None
        for block in self.chain:
            if block['hash'] == block_hash:
                correct_block = block
                break
        return correct_block

    def get_transaction(self, transaction_id):
        correct_transaction = None
        correct_block = None
        for block in self.chain:
            for transaction in block['transactions']:
                if transaction['transaction_id'] == transaction_id:
                    correct_transaction = transaction
                    correct_block = block
                    break
            if correct_transaction:
                break
        return {
            'transaction': correct_transaction,
            'block': correct_block
        }

    def get_address_data(self, address):
        address_transactions = []
        for block in self.chain:
            for transaction in block['transactions']:
                if transaction['sender'] == address or transaction['recipient'] == address:
                    address_transactions.append(transaction)

        balance = 0
        for transaction in address_transactions:
            if transaction['recipient'] == address:
                balance += transaction['amount']
            elif transaction['sender'] == address:
                balance -= transaction['amount']

        return {
            'addressTransactions': address_transactions,
            'addressBalance': balance
        }

