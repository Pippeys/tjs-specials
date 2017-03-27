#python3
#https://www.alltrails.com/us/california/backpacking scraping for locations

import bs4 as bs
import urllib.request
import csv
import lxml
import itertools


def build_list(trail_data):
    trail_list=[]
    for a in trail_data:
        trail_name = (a.text)
        trails = [trail_name]
        trail_list.append(trails)
    return trail_list


def write_csv (trail_list, rating_list):
    with open('Trail_list.csv', 'wb') as file:
        writer = csv.writer(file)
        writer.writerows(zip(trail_list, rating_list))


def star_rating(rating_data):
    rating_list = []
    for span in rating_data:
        rating = (span.text)
        rating_stars = [rating]
        rating_list.append(rating_stars)

    return rating_list


def main():
    trail_sauce = urllib.request.urlopen('https://www.alltrails.com/us/california/backpacking').read()
    trail_soup = bs.BeautifulSoup(trail_sauce, 'lxml')
    trail_data = trail_soup.find_all('a', class_='link mobile-block')
    rating_data = trail_soup.find_all('span', itemprop='reviewRating')
    trail_list = build_list(trail_data)
    write_csv(trail_list, rating_list)



if __name__ == "__main__":
	main()
