from flask import Flask, jsonify, request
from uuid import uuid4
from src.blockchain import Blockchain
from dotenv import dotenv_values

config = dotenv_values(".env")

app = Flask(__name__)
node_address = str(uuid4()).replace('-', '')
blockchain = Blockchain()


@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)

    block = blockchain.create_block(proof, previous_hash)

    response = {'message': 'Congratulations you mined a block!',
                'index': block['index'], 'timestamp': block['timestamp'],
                'proof': block['proof'], 'previous_hash': block['previous_hash'],
                'transaction': block['transactions']}

    return jsonify(response), 200


@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain': blockchain.chain, 'length': len(blockchain.chain)}
    return jsonify(response), 200


@app.route('/is_valid', methods=['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'All right, the blockchain is valid'}
    else:
        response = {'message': 'The blockchain is invalid'}
    return jsonify(response), 200


@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    transaction = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount']
    if not all(key in transaction for key in transaction_keys):
        return 'Missing some elements', 400

    index = blockchain.add_transaction(
        transaction['sender'], transaction['receiver'], transaction['amount'])

    response = {'message': f'This transaction will be add at block {index}'}
    return jsonify(response), 201


@app.route('/connect_node', methods=['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')

    if nodes is None:
        return 'Empty nodes', 400

    for node in nodes:
        blockchain.add_nodes(node)

    response = {'message': 'All nodes are connected',
                'total_nodes': list(blockchain.nodes)}
    return jsonify(response), 201


@app.route('/replace_chain', methods=['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()

    if is_chain_replaced:
        response = {'message': 'The nodes had different chains, so will be replaced',
                    'new_chain': blockchain.chain}
    else:
        response = {'message': 'All chains are right, not will be replaced'}

    return jsonify(response), 201


# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=config.APP_PORT)
