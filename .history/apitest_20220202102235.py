
import json

thecloud = json.loads(open('thecloud.json').read())

# print(thecloud["Blocks"])
# print(thecloud["Blocks"][-1]["Amount"])

for block in thecloud["Blocks"]:
    print(block)
