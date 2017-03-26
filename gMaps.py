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

	print(json.dumps(places_result, indent=4))
	print("\n########################################################################\n")
	print(lat)
	print("Longitude:")
	print(lng)

	return lat, lng


def main():

	api_key = get_api_key()

	location = input("What location are you looking for?:")

	get_gps_coords(location, api_key)
	#get_address(location, api_key)


if __name__ == "__main__":
	main()
