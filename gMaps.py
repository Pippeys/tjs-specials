import googlemaps
from datetime import datetime
import pprint, json, os


# Get API key from file stored in GithubPrivates folder outside of Github repos

with open(os.getcwd() + "\\..\\..\\GithubPrivates\\googleapikey.txt","r") as myfile:
	APIKey = myfile.read()

gmaps = googlemaps.Client(key=APIKey)

# Geocoding an address
geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

print(json.dumps(geocode_result, indent=4))
print("\n########################################################################\n")
print("Latitude:")
print(geocode_result[0]['geometry']['location']['lat'])
print("Longitude:")
print(geocode_result[0]['geometry']['location']['lng'])
