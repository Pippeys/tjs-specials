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


def main():

	api_key = get_api_key()

	location = input("What location are you looking for?:")

	lat, lng, addr = get_gps_coords(location, api_key)

	print("Location: " + addr)
	print("Latitude: " + str(lat))
	print("Longitude: " + str(lng))


if __name__ == "__main__":
	main()
