import datetime
from urllib.parse import urlparse
import requests
from proof_of_work import ProofOfWork


class Blockchain(ProofOfWork):
    def __init__(self):
        self.chain = []
        self.transctions = []
        self.create_block(proof=1, previous_hash='0')
        self.nodes = set()

    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof, 'previous_hash': previous_hash,
                 'transactions': self.transctions}
        self.transctions = []
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False

    def add_transaction(self, sender, receiver, amount):
        self.transctions.append(
            {'sender': sender, 'receiver': receiver, 'amount': amount})
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1

    def add_nodes(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
