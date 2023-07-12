# Import the modules
import requests
import json

# Define a business ID
#business_id = '4AErMBEoNzbk7Q8g45kKaQ'
#unix_time = 1546047836

url = "https://api.yelp.com/v3/businesses/search"
# Define my API Key, My Endpoint, and My Header
API_KEY = ''
#ENDPOINT = 'https://api.yelp.com/v3/businesses/{}/reviews'.format(business_id)
ENDPOINT = 'https://api.yelp.com/v3/businesses/search'
HEADERS = {'Authorization': 'bearer %s' % API_KEY}

# Define my parameters of the search
# BUSINESS SEARCH PARAMETERS - EXAMPLE


# BUSINESS MATCH PARAMETERS - EXAMPLE
#PARAMETERS = {'name': 'Peets Coffee & Tea',
#              'address1': '7845 Highland Village Pl',
#              'city': 'San Diego',
#              'state': 'CA',
#              'country': 'US'}

# Make a request to the Yelp API
data = {"businesses":[]}
for i in range(20):
    PARAMETERS = {'term': 'thai',
             'limit': 50,
             'offset': 50*i,
             'radius': 40000,
             'location': 'New York'}
    response = requests.get(url = ENDPOINT,
                            params = PARAMETERS,
                            headers = HEADERS)

    # Convert the JSON String
    business_data = response.json()
    data["businesses"].extend(business_data["businesses"]) 

json_object = json.dumps(data, indent = 4)
with open('thai_yelp.json','w') as outfile:
    outfile.write(json_object)

# print the response
#print(json.dumps(business_data, indent = 3))
