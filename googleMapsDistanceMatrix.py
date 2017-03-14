'''
This script reads a list of addresses and uses the Google Maps
Distance Matrix API to determine the distance and travel time
between every address and every other address.

Dependencies:
requests

Input files (saved in same directory as script):
addresses.txt (one address per line)
google_dm_key.txt (contains Google Maps Distance Matrix API key)

Output:
Prints tab-delimited tables, with destination addresses listed along
the top, starting addresses along the left column, and values populated
within. Prints three tables: distance, travel time, and distance + time.
'''

import requests

# File containing one address per line
with open('addresses.txt', 'r') as f:
    addresses = [x.strip() for x in f.readlines()]
joinedAddresses = "|".join(addresses)
blanklist = ["",]

# File containing the Google Maps Distance Matrix API key
with open('google_dm_key.txt', 'r') as g:
    apiKey = g.read().strip()

url = "https://maps.googleapis.com/maps/api/distancematrix/json"
params = {
    'origins': joinedAddresses,
    'destinations': joinedAddresses,
    'key': apiKey,
    'units': "imperial",
}
r = requests.get(url, params).json()

# Distance (Miles)
print("\t".join(blanklist+addresses))
rowCounter = 0
for row in r['rows']:
    results = []
    results.append(addresses[rowCounter])
    for element in row['elements']:
        distance = element['distance']['text']
        duration = element['duration']['text']
        results.append('{d}'.format(d=distance))
    print("\t".join(results))
    rowCounter += 1

print()

# Travel Time (Hours and Minutes)
print("\t".join(blanklist+addresses))
rowCounter2 = 0
for row in r['rows']:
    results = []
    results.append(addresses[rowCounter2])
    for element in row['elements']:
        distance = element['distance']['text']
        duration = element['duration']['text']
        results.append('{t}'.format(t=duration))
    print("\t".join(results))
    rowCounter2 += 1

print()

# Mileage and Travel Time
print("\t".join(blanklist+addresses))
rowCounter3 = 0
for row in r['rows']:
    results = []
    results.append(addresses[rowCounter3])
    for element in row['elements']:
        distance = element['distance']['text']
        duration = element['duration']['text']
        results.append('{d} ({t})'.format(d=distance, t=duration))
    print("\t".join(results))
    rowCounter3 += 1

