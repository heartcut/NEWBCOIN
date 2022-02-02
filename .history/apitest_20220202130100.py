
import json
import hashlib
import codecs

thecloud = json.loads(open('thecloud.json').read())

# print(thecloud["Blocks"])
# print(thecloud["Blocks"][-1]["Amount"])
balance = 0
for block in thecloud["Blocks"]:
    if block["Reciever"] == "981e73919b4c409b5e0a71a2a691d9414bafba1cae8636ac0b1a276dce679f8a":
        balance = balance + int(block["Amount"])
print(hashlib.md5(str(thecloud["Blocks"][-1]).encode()).hexdigest())


trytoanswer = requests.request(
    "GET", solveurl+str(publickeystringvar.get())+"&answer="+str(guess[q]+guess[w]+guess[e]+guess[r]))
if json.loads(trytoanswer.text) == "True":
    gotthecoin = True
    raise StopIteration
else:
    gotthecoin = False
    raise StopIteration
