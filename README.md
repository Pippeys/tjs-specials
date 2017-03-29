# Jordan-[Scott](https://github.com/Pippeys)-[Ted](https://github.com/Sarulian) Test Repository

This is a repository just for us to try out coordinating a project on Github

## Current Project Idea
Camping locations webscraper

### User Use:

- For people looking to find new trails and campsites
- Using an EXTREMELY advanced algorithm (lol) to find unpopular and highly rated locations  
- Giving descriptions, locations, and pictures

Outline:
- Get picture + name of location from https://www.alltrails.com/us/california/backpacking
- Get gps coordinates from name and google maps api
- Use Geosphere library for mapping?
- Plot locations and pictures onto custom google map
- ????
- Profit!

## To get google maps api credentials

- Follow directions at https://github.com/googlemaps/google-maps-services-python
- Get an API key and save it as a text file called "googleapikey.txt" in a directory called "\GithubPrivates" next to "\Github"
- Enable API services "Geocoding"
- Don't forget to "pip install -U googlemaps"


## Running LocationFinder.py creates the list of trails

- Be sure to have modules: bs4, urllib.request, csv, lxml, pandas



## To-Do

- Integrate google trends for popularity scaling
- Load more button 
