#python3
#https://www.alltrails.com/us/california/backpacking scraping for locations

import bs4 as bs
import urllib.request
import csv
import lxml



def build_list(trail_data):
    trail_list=[]
    for a in trail_data:
        trail_name = (a.text)
        trails = [trail_name]
        trail_list.append(trails)
    return trail_list

def write_csv (trail_list):
    with open('Trail_list.csv', 'w') as file:
        csv_writer = csv.writer(file)
        for row in trail_list:
            csv_writer.writerow(row)

def main():
    trail_sauce = urllib.request.urlopen('https://www.alltrails.com/us/california/backpacking').read()
    trail_soup = bs.BeautifulSoup(trail_sauce, 'lxml')
    trail_data = trail_soup.find_all('a', class_='link mobile-block')



    trail_list = build_list(trail_data)
    write_csv(trail_list)


if __name__ == "__main__":
	main()
