from flask import Flask
import json
import hashlib
import time
from flask import request
import random
import string

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/api/', methods=['GET'])
def api_all():
    f = open('thecloud.json')
    return json.load(f)


@app.route('/api/statuscheck/', methods=['GET'])
def api_status():
    return json.dumps(True)


@app.route('/api/balancecheck', methods=['GET'])
def api_balance_check():
    page = request.args.get('pubkey', default=1, type=str)
    thecloud = json.loads(open('thecloud.json').read())
    balance = 0
    for block in thecloud["Blocks"]:
        if block["Reciever"] == page:
            balance = balance + int(block["Amount"])
    return json.dumps(balance)


serverdata = open('serverdata.txt', 'r')
currentpow = str(serverdata.read())
serverdata.close()


@app.route('/api/solveblock', methods=['GET'])
def attempt_to_solve():
    answer = request.args.get('answer', default=1, type=str)
    pubkey = request.args.get('pubkey', default=1, type=str)
    if answer == currentpow:
        add_new_block(pubkey)


def add_new_block(pubkey):
    thecloud = json.loads(open('thecloud.json').read())
    newblocknumber = int(thecloud["Blocks"][-1]["BlockNumber"])+1
    hashoflastblock = hashlib.md5(
        str(thecloud["Blocks"][-1]).encode()).hexdigest()
    newpow = ''.join(random.choice(string.ascii_letters) for x in range(4))
    serverdata = open('walletdata.txt', 'w')
    serverdata.write(newpow)
    serverdata.close()
    hashedpow = (hashlib.md5(newpow.encode())).hexdigest()
    newblock = {
        "LastHash": hashoflastblock,
        "POWhash": hashedpow,
        "Reciever": pubkey,
        "Sender": "Transaction",
        "Time": "timehere",
        "BlockNumber": str(newblocknumber),
        "Type": "BlockSolved",
        "Amount": "1"
    }

##############################################
# below is unused code for now


class Block(object):
    def __init__(self, LastHash, POWhash, Reciever, Sender, Time, BlockNumber, Type, Amount, timestamp=None):
        self.LastHash = LastHash
        self.POWhash = POWhash
        self.Reciever = Reciever
        self.Sender = Sender
        self.Time = Time
        self.BlockNumber = BlockNumber
        self.Type = Type
        self.Amount = Amount
        #self.timestamp = timestamp or time.time()
    # @property
    # def compute_hash(self):
    #     string_block = "{}{}{}{}{}".format(self.index, self.proof_number, self.previous_hash, self.data, self.timestamp)
    #     return hashlib.sha256(string_block.encode()).hexdigest()
    # def __repr__(self):
    #     return "{} - {} - {} - {} - {}".format(self.index, self.proof_number, self.previous_hash, self.data, self.timestamp)


class BlockChain(object):
    def __init__(self):
        self.chain = []  # json file
        self.current_data = []
        self.nodes = set()
        self.build_genesis()
    # def build_genesis(self):
    #     block = Block(
    #         index=len(self.chain),
    #         proof_number=0,
    #         previous_hash="no previos hash",
    #         data={'sender': "thecreator",'receiver': "thechain",'amount': "100"}
    #     )
    #     self.chain.append(block)

    def build_block(self, proof_number, previous_hash):
        block = Block(
            index=len(self.chain),
            proof_number=proof_number,
            previous_hash=previous_hash,
            data=self.current_data
        )
        self.current_data = []
        self.chain.append(block)
        return block

    @staticmethod
    def confirm_validity(block, previous_block):
        if previous_block.index + 1 != block.index:
            return False
        elif previous_block.compute_hash != block.previous_hash:
            return False
        elif block.timestamp <= previous_block.timestamp:
            return False
        return True

    def get_data(self, sender, receiver, amount):
        self.current_data.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        })
        return True

    @staticmethod
    def proof_of_work(last_proof):
        pass

    @property
    def latest_block(self):
        return self.chain[-1]

    def chain_validity(self):
        pass
    # def block_mining(self, details_miner):
    #     self.get_data(
    #         sender="0", #it implies that this node has created a new block
    #         receiver=details_miner,
    #         quantity=1, #creating a new block (or identifying the proof number) is awared with 1
    #     )
    #     last_block = self.latest_block
    #     last_proof_number = last_block.proof_number
    #     proof_number = self.proof_of_work(last_proof_number)
    #     last_hash = last_block.compute_hash
    #     block = self.build_block(proof_number, last_hash)
    #     return vars(block)
    # def create_node(self, address):
    #     self.nodes.add(address)
    #     return True
    # @staticmethod

    def get_block_object(block_data):
        return Block(
            block_data['index'],
            block_data['proof_number'],
            block_data['previous_hash'],
            block_data['data'],
            timestamp=block_data['timestamp']
        )