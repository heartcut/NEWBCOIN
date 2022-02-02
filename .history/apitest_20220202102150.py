
import json

thecloud = json.loads(open('thecloud.json').read())

print(thecloud["Blocks"][-1]["BlockNumber"])
print(thecloud["Blocks"][-1]["Amount"])
