from hash import Hash


class ProofOfWork(Hash):
    def is_chain_valid(chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            current_block = chain[block_index]
            if current_block['previous_hash'] != previous_block['hash']:
                return False
            previous_block = current_block
            block_index += 1
        return True

    def is_valid_hash(hash):
        int_hash = Hash.int_hash(hash)
        if str(int_hash)[:4] != '0000':
            return False
        return True
