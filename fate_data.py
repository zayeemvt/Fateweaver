import json

filename = "server_data.json"

def saveData(object):
    data = json.dumps(object, default=lambda o: o.__dict__, indent=4, sort_keys=True)
    
    with open(filename, "w") as outfile:
        outfile.write(data)

def loadData():
    with open(filename, 'r') as openfile:
        return json.load(openfile)