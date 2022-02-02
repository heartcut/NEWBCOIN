
import json
import hashlib
import codecs
import requests

thecloud = json.loads(open('thecloud.json').read())

# print(thecloud["Blocks"])
# print(thecloud["Blocks"][-1]["Amount"])
balance = 0
for block in thecloud["Blocks"]:
    if block["Reciever"] == "981e73919b4c409b5e0a71a2a691d9414bafba1cae8636ac0b1a276dce679f8a":
        balance = balance + int(block["Amount"])
# print(hashlib.md5(str(thecloud["Blocks"][-1]).encode()).hexdigest())


trytoanswer = requests.request(
    "GET", 'http://127.0.0.1:5000//api/solveblock?pubkey=93ad8e103e0a7f4d6a64045ab28320bd9ec1c66d880197947e994d028de62bf6c1a975facfdb0a0c8e6c9f03277ac85ed939de84024812d0f63ee831f55f457f&answer=JJyZ')

print(json.loads(trytoanswer.text))
# if json.loads(trytoanswer.text) == "True":
#     print("true")
# else:
#     print("false")
