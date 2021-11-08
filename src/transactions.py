class Transaction:
    def add_transaction(self, sender, receiver, amount):
        self.transctions.append(
            {'sender': sender, 'receiver': receiver, 'amount': amount})
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1
