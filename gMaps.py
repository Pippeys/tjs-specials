import googlemaps
from datetime import datetime
import pprint, json, os
import makeMap
import csv


# Get API key from file stored in GithubPrivates folder outside of Github repos
def get_api_key():

	with open(os.getcwd() + "\\..\\..\\GithubPrivates\\googleapikey.txt","r") as myfile:
		api_key = myfile.read()

	return api_key


def get_gps_coords(location, api_key, gmaps_client):

	# Geocoding an address
	places_result = gmaps_client.places(location)

	#print(json.dumps(places_result, indent=4))

	if (places_result["status"] == "OK"):
		lat = places_result["results"][0]['geometry']['location']['lat']
		lng = places_result["results"][0]['geometry']['location']['lng']
		address = places_result["results"][0]['formatted_address']

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


def generate_map(gps_coords):

	map = makeMap.Map()

	for point in gps_coords:
		map.add_point((point[0], point[1]))

	with open("output.html", "w") as out:
		print(map, file=out)


def get_names_from_csv():

	names = []
	mycsv = csv.reader(open(".\\Trail_list.csv"))

	for row in mycsv:
		if (row):
			names.append(row[0])

	return names


def main():

	api_key = get_api_key()
	gmaps = googlemaps.Client(key=api_key)

	names = get_names_from_csv()

	gps_coords = []
	for name in names:
		coords = get_gps_coords(clean_name(name), api_key, gmaps)
		if (coords):
			gps_coords.append(coords)

	print(gps_coords)

	generate_map(gps_coords)


if __name__ == "__main__":
	main()
