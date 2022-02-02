
import json

thecloud = json.loads(open('thecloud.json').read())

print(thecloud["Blocks"])
print(thecloud["Blocks"][-1]["Amount"])
