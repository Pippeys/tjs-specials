import googlemaps
from datetime import datetime
import pprint, json, os


# Get API key from file stored in GithubPrivates folder outside of Github repos
def get_api_key():

	with open(os.getcwd() + "\\..\\..\\GithubPrivates\\googleapikey.txt","r") as myfile:
		api_key = myfile.read()

	return api_key


def get_gps_coords(location, api_key):

	gmaps = googlemaps.Client(key=api_key)

	# Geocoding an address
	places_result = gmaps.places(location)

	lat = places_result["results"][0]['geometry']['location']['lat']
	lng = places_result["results"][0]['geometry']['location']['lng']
	address = places_result["results"][0]['formatted_address']

	#print(json.dumps(places_result, indent=4))

	return lat, lng, address


# Remove keywords like "via" and "to" and only use the location name
def clean_name(location):

	via_loc = int(location.find(" via "))
	to_loc = int(location.find(" to "))

	if (via_loc != -1):
		location = location[0:via_loc]

	if (to_loc != -1):
		location = location[to_loc + 4:]

	return location


def main():

	api_key = get_api_key()

	#just for testing
	location = input("What location are you looking for?:")

	location = clean_name(location)

	lat, lng, addr = get_gps_coords(location, api_key)

	print("Location: " + addr)
	print("Latitude: " + str(lat))
	print("Longitude: " + str(lng))


if __name__ == "__main__":
	main()
