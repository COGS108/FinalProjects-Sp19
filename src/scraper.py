import requests
import bs4
from bs4 import BeautifulSoup
import csv
import pandas as pd

def storeData(url, rating, variance, id_num):
	page = requests.get(url)
	soup = BeautifulSoup(page.text, features="html.parser")

	# Skip if page is not found
	header = soup(id="maincontent")[0].find('h2').getText()
	if header == "Sorry, page not found":
		print("Skipping id=" + id_num)
		return

	# Include ID
	print('ID: ' + str(id_num))

	# Retrieve place name
	place = soup(itemtype="schema.org/Photograph")[0].find('h2').contents[1]
	place = place[3:]
	print('Place: ' + place)

	# Include Rating
	print('Rating: ' + rating)

	# Include Variance
	print('Variance: ' + variance)

	# Retrieve near area (village, city, etc.)
	near = soup(itemprop="contentLocation")[0].findAll('b', text=True)[-1].getText()
	print('Near: ' + near)

	# Retrieve county
	county = soup(itemprop="contentLocation")[0].find('i', text=True).getText()
	county = county.split(',')[1]
	county = county[1:]
	print('County: ' + county)

	# Retrieve category
	category = soup(itemprop="keywords") or ''
	if category != '':
		category = category[0].getText()
	print("Category: " + category)

	# Retrieve image
	image = soup(itemprop="contentURL")[0]['src']
	print("Image: " + image)

	# Retrieve date taken
	dateData = soup(itemprop="exifData") or soup(itemprop="uploadDate")
	date = dateData[0].getText()
	print("Date: " + date)

	# Include URL
	print("URL: " + url)

	filewriter.writerow([id_num, place, rating, variance, near, county, category, image, date, url])


# Open csv
csvfile = open('scenery.csv', 'a', encoding='utf-8')
filewriter = csv.writer(csvfile, lineterminator = '\n')

# Checkpoint starts the program loop starting with that id number
df = pd.read_csv('scenery.csv', encoding='ISO-8859-1')
if len(df) == 0:
	checkpoint_id = -1
else:
	#checkpoint_id = df['ID'][len(df['ID']) - 1] + 1
        checkpoint_id = 217675

# Store all urls and ratings
if checkpoint_id == -1:
	filewriter.writerow(['ID', 'Place', 'Rating', 'Variance', 'Near', 'County', 'Category', 'Image', 'Date', 'URL'])
with open('./votes.tsv', 'r') as fp:
	for count, line in enumerate(fp):
		if count != 0:
			data = line.split('\t')
			id_num = data[0]

			if int(id_num) >= checkpoint_id:
				rating = data[4]
				variance = data[3]
				url = data[6]
				storeData(url, rating, variance, id_num)
				print()

fp.close()
