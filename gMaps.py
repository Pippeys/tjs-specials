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
	geocode_result = gmaps.geocode(location)

	lat = geocode_result[0]['geometry']['location']['lat']
	lng = geocode_result[0]['geometry']['location']['lng']

	print(json.dumps(geocode_result, indent=4))
	print("\n########################################################################\n")
	print("Latitude:")
	print(lat)
	print("Longitude:")
	print(lng)

	return lat, lng


def main():

	api_key = get_api_key()

	location = input("What location are you looking for?:")

	get_gps_coords(location, api_key)


if __name__ == "__main__":
	main()
