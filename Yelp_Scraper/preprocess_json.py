import json
all_records = []
with open('chinese_yelp.json','r') as datafile:
    records = json.load(datafile)
    records = records['businesses']
new_records = []
for i in records:
    new_dic = {}
    new_dic["id"]=i["id"]
    new_dic["cuisine"] = "chinese"
    new_records.append(new_dic)

all_records.extend(new_records)

with open('italian_yelp.json','r') as datafile:
    records = json.load(datafile)
    records = records['businesses']

new_records = []
for i in records:
    new_dic = {}
    new_dic["id"]=i["id"]
    new_dic["cuisine"] = "italian"
    new_records.append(new_dic)
all_records.extend(new_records)

with open('indian_yelp.json','r') as datafile:
    records = json.load(datafile)
    records = records['businesses']

new_records = []
for i in records:
    new_dic = {}
    new_dic["id"]=i["id"]
    new_dic["cuisine"] = "indian"
    new_records.append(new_dic)
all_records.extend(new_records)

with open('mexican_yelp.json','r') as datafile:
    records = json.load(datafile)
    records = records['businesses']

new_records = []
for i in records:
    new_dic = {}
    new_dic["id"]=i["id"]
    new_dic["cuisine"] = "mexican"
    new_records.append(new_dic)
all_records.extend(new_records)

with open('thai_yelp.json','r') as datafile:
    records = json.load(datafile)
    records = records['businesses']

new_records = []
for i in records:
    new_dic = {}
    new_dic["id"]=i["id"]
    new_dic["cuisine"] = "thai"
    new_records.append(new_dic)
all_records.extend(new_records)

with open('american_yelp.json','r') as datafile:
    records = json.load(datafile)
    records = records['businesses']

new_records = []
for i in records:
    new_dic = {}
    new_dic["id"]=i["id"]
    new_dic["cuisine"] = "american"
    new_records.append(new_dic)
all_records.extend(new_records)

print(len(all_records))
print(all_records[900])
print(all_records[1500])
print(all_records[2500])
print(all_records[3500])
print(all_records[4500])
print(all_records[5500])

"""
outfile = open("combined_new.json",'w')
for i in all_records:
    outfile.write(str(i)+"\n")
"""

json_obj = json.dumps(all_records)
with open("combined_json.json",'w') as outfile:
    outfile.write(json_obj)




"""
#def generate_es_data(file_path):
global GLOBAL_INDEX
restaurants = json.load(open(file_path))
ndjson = ""
for rstr in restaurants:
    source = {
        'id': rstr['id'],
        'category': rstr['category']
    }
    action = {"index":{"_id":str(GLOBAL_INDEX)}}
    GLOBAL_INDEX += 1

    ndjson += json.dumps(action) + '\n' + json.dumps(source) + '\n'

return ndjson
"""