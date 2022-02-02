
import json

thecloud = json.loads(open('thecloud.json').read())

# print(thecloud["Blocks"])
# print(thecloud["Blocks"][-1]["Amount"])

for block in thecloud["Blocks"]:
    if block["Reciver"] == "981e73919b4c409b5e0a71a2a691d9414bafba1cae8636ac0b1a276dce679f8a":
        print(block["Amount"])
    print(block)
