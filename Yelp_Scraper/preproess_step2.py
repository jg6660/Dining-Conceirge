import json

GLOBAL_INDEX = 1
infile = open('combined_json.json','r')
restaurants = json.load(infile)
ndjson = ""
for rstr in restaurants:
    source = {
        'id': rstr['id'],
        'cuisine': rstr['cuisine']
    }
    action = {"index":{"_id":str(GLOBAL_INDEX)}}
    GLOBAL_INDEX += 1

    ndjson += json.dumps(action) + '\n' + json.dumps(source) + '\n'


obj = json.dumps(ndjson)
with open("final.json",'w') as outfile:
    outfile.write(obj)