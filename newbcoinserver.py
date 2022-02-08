from flask import Flask
import json
import hashlib
import time
from flask import request
import random
import string
import time
from ecdsa import SigningKey, SECP256k1, VerifyingKey
import codecs
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


@app.route('/api/getlastblock/', methods=['GET'])
def get_last_block():
    thecloud = json.loads(open('thecloud.json').read())
    return json.dumps(thecloud["Blocks"][-1])


@app.route('/api/solveblock', methods=['GET'])
def attempt_to_solve():
    serverdata = open('serverdata.txt', 'r')
    currentpow = str(serverdata.read())
    serverdata.close()
    answer = request.args.get('answer', default=1, type=str)
    pubkey = request.args.get('pubkey', default=1, type=str)
    if answer == currentpow:
        add_new_block(pubkey)
        return json.dumps(True)
    else:
        return json.dumps(False)


@app.route('/api/dotransaction', methods=['GET'])
def settransaction():
    mykey = request.args.get('mykey', default=1, type=str)
    reckey = request.args.get('reckey', default=1, type=str)
    amount = request.args.get('amount', default=1, type=str)
    transactionhash = request.args.get('transactionhash', default=1, type=str)
    thecloudfile = open('thecloud.json', 'r+')
    theclouddata = json.load(thecloudfile)

    newblocknumber = int(theclouddata["Blocks"][-1]["BlockNumber"])+1

    hashoflastblock = hashlib.md5(
        str(theclouddata["Blocks"][-1]).encode()).hexdigest()

    hashedpow = theclouddata["Blocks"][-1]["POWhash"]

    mytime = time.time()

    publickey = VerifyingKey.from_string(bytes.fromhex(
        mykey), curve=SECP256k1)

    transblock = "Reciever:"+reckey+",Amount:"+amount
    print(transblock)
    try:
        if publickey.verify(bytes.fromhex(transactionhash), str.encode(transblock)):
            newblock = {
                "LastHash": hashoflastblock,
                "POWhash": hashedpow,
                "Reciever": reckey,
                "Sender": mykey,
                "Time": mytime,
                "BlockNumber": str(newblocknumber),
                "Type": "Transaction",
                "Amount": amount,
                "HashOfTransaction": transactionhash
            }
            theclouddata["Blocks"].append(newblock)
            thecloudfile.seek(0)
            json.dump(theclouddata, thecloudfile, indent=4)
            return json.dumps(True)
        else:
            return json.dumps(False)
    except:
        return json.dumps(False)


def add_new_block(pubkey):
    thecloudfile = open('thecloud.json', 'r+')
    theclouddata = json.load(thecloudfile)
    newblocknumber = int(theclouddata["Blocks"][-1]["BlockNumber"])+1
    hashoflastblock = hashlib.md5(
        str(theclouddata["Blocks"][-1]).encode()).hexdigest()
    newpow = ''.join(random.choice(string.ascii_letters) for x in range(4))
    serverdata = open('serverdata.txt', 'w')
    serverdata.write(newpow)
    serverdata.close()
    hashedpow = (hashlib.md5(newpow.encode())).hexdigest()
    mytime = time.time()
    newblock = {
        "LastHash": hashoflastblock,
        "POWhash": hashedpow,
        "Reciever": pubkey,
        "Sender": "0",
        "Time": mytime,
        "BlockNumber": str(newblocknumber),
        "Type": "BlockSolved",
        "Amount": "1",
        "HashOfTransaction": "0"
    }
    theclouddata["Blocks"].append(newblock)
    thecloudfile.seek(0)
    json.dump(theclouddata, thecloudfile, indent=4)

##############################################
