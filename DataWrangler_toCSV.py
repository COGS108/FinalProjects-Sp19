from datetime import date, datetime, timedelta
import csv
import inquirer
from bs4 import BeautifulSoup
import requests
import time
import urllib2
import json
import re
import unicodedata

lyric_dict = dict()
nan = 0

charts = {'Hot 100': ["https://www.billboard.com/charts/hot-100/", 1958, 8, 4],
          'Pop Songs': ["https://www.billboard.com/charts/pop-songs/", 1992, 10, 3],
          'Rock Songs': ["https://www.billboard.com/charts/rock-songs/", 2009, 6, 20],
          'Hip-Hop/R&B Songs': ["https://www.billboard.com/charts/r-b-hip-hop-songs/", 1958, 10, 20],
          'Country Songs': ["https://www.billboard.com/charts/country-songs/", 1958, 10, 20]
          }


def info(s, dt):
    artist = s.get("data-artist").encode('ascii', 'ignore').decode('ascii')
    song = s.get("data-title").encode('ascii', 'ignore').decode('ascii')
    rank = s.get("data-rank")
    lyrics = get_lyrics(song, artist).encode('ascii', 'ignore').decode('ascii')
    if s.find(class_="chart-list-item__last-week") is None:
        last = '0'
    else:
        last = s.find(class_="chart-list-item__last-week").contents[0]
    if s.find(class_="chart-list-item__weeks-at-one") is None:
        peak = '0'
    else:
        peak = s.find(class_="chart-list-item__weeks-at-one").contents[0]
    if s.find(class_="chart-list-item__weeks-on-chart") is None:
        weeks = '0'
    else:
        weeks = s.find(class_="chart-list-item__weeks-on-chart").contents[0]
    return [artist, song, dt.isoformat(), rank, last, peak, weeks, lyrics]


def scrape_site(writer, url, chart_date):
    global nan
    new_url = url + chart_date.isoformat()
    req = requests.get(new_url)
    start_time = time.time()
    soup = BeautifulSoup(req.text, "html.parser")
    songs = soup.find_all(class_="chart-list-item")
    hundred_list = [info(x, chart_date) for x in songs]
    print("Time taken: " + str(time.time() - start_time))
    print("NaNs = " + str(nan) + " out of " + str(len(lyric_dict)) + "total songs")
    writer.writerows(hundred_list)
    if (time.time() - start_time) < 1:
        time.sleep(1 - (time.time() - start_time))


def song_cleaner(song):
    song = song.lower()
    song_array = song.split(" (")
    song = song_array[0]
    song = song.replace('-', ' ')
    song = re.sub(r'([^\s\w]|_)+', '', song)
    return song


def get_lyrics(song, artist):
    global nan
    global lyric_dict
    # Makes a URL that the genius API is capable of reading/requesting
    genius_url = "https://api.genius.com/search?q="

    # Clean up the artist name a little
    artist = artist.replace("&", "and")
    artist = artist.replace("And", "and")
    artist = artist.replace("-", " ")
    artist_array = re.split(" with the", artist, flags=re.IGNORECASE)
    artist = artist_array[0]
    artist_array = re.split(" and the", artist, flags=re.IGNORECASE)
    artist = artist_array[0]
    artist_array = re.split(" with his", artist, flags=re.IGNORECASE)
    artist = artist_array[0]
    artist_array = re.split(" and his", artist, flags=re.IGNORECASE)
    artist = artist_array[0]

    artist_array = artist.split()

    unicodedata.normalize('NFD', song).encode('ascii', 'ignore')
    song = song_cleaner(song)
    unicodedata.normalize('NFD', artist).encode('ascii', 'ignore')
    # Handles case where name is really long (i.e. "Johnny Cash and the ...")
    # Handles case where name is long and first word starts with "The" (i.e. "The Arctic Monkeys")
    if len(artist_array) > 2:
        if artist_array[0] == 'The':
            artist = artist_array[1] + ' ' + artist_array[2]
        elif artist_array[1] == "and":
            artist = artist_array[0] + ' ' + artist_array[2]
        else:
            artist = artist_array[0] + ' ' + artist_array[1]
    searchable_artist = artist.replace(' ', '%20')
    searchable_song = song.replace(' ', '%20').replace(',', '')

    # url to search lyrics for
    url = genius_url + searchable_artist + '%20' + searchable_song

    #Dont access genius more than once for the same song
    if url in lyric_dict:
        lyrics = lyric_dict.get(url)
        return lyrics

    # Searching desired request
    req = urllib2.Request(url)
    req.add_header("Authorization", "Bearer " + 'yiADkgc2eQhp8sA4BcPF55CJDFYKFK44gsmMnblPMiFZVmf448KEtwVFqipu5qlT')
    req.add_header("User-Agent", "")
    # req.json()

    # Results of the search for "artist" + "song" in JSON format
    res = urllib2.urlopen(req, timeout=30)
    start_time = time.time()
    # answer = res.json()
    search = json.loads(res.read())
    lyric_url = ''
    # Loop through search results
    for result in search['response']['hits']:
        artist_name = unicodedata.normalize('NFD', result['result']['primary_artist']['name']).encode('ascii',
                                                                                                      'ignore').decode(
            'ascii')
        song_name = unicodedata.normalize('NFD', result['result']['title']).encode('ascii', 'ignore').decode('ascii')
        song_name = song_cleaner(song_name)
        if artist_name == artist:
            if song_name == song:
                lyric_url = result['result']['url'].encode('ascii', 'ignore').decode('ascii')
                break
            else:
                song_words = song.split()
                song_shared = 0
                for x in range(len(song_words)):
                    if song_words[x] in song_name:
                        song_shared = song_shared + 1
                if song_shared == len(song_words):
                    lyric_url = result['result']['url'].encode('ascii', 'ignore').decode('ascii')
                    break
                    time.wait()
        else:
            artist_words = artist.split()
            artist_shared = 0
            for y in range(len(artist_words)):
                if artist_words[y] in artist_name:
                    artist_shared = artist_shared + 1
            if artist_shared == len(artist_words):
                song_words = song.split()
                song_shared = 0
                for x in range(len(song_words)):
                    if song_words[x] in song_name:
                        song_shared = song_shared + 1
                if song_shared == len(song_words):
                    lyric_url = result['result']['url'].encode('ascii', 'ignore').decode('ascii')
                    break
    if lyric_url == '':
        nan += 1
        lyric_dict[url] = 'NaN'
        if (time.time() - start_time) < 1:
            time.sleep(1 - (time.time() - start_time))
        return 'NaN'
    else:
        lyrics = get_lyrics_from_url(lyric_url)
        lyric_dict[url] = lyrics
        if (time.time() - start_time) < 1:
            time.sleep(1 - (time.time() - start_time))
        return lyrics


def get_lyrics_from_url(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")
    lyr = soup.find("div", {"class": "lyrics"})
    try:
        lyrics = lyr.get_text()
    except AttributeError:
        lyrics = "NaN"
    return lyrics


def date_increment(d):
    dt = datetime(d.year, d.month, d.day)
    week = timedelta(days=7)
    inc = dt + week
    return inc.date()


def last_day():
    today = datetime.today()
    day = today.weekday()
    if day == 6:
        return today.date()
    sub = timedelta(days=(day + 1))
    previous_sunday = today - sub
    last = timedelta(days=13)
    last_date = previous_sunday + last
    return last_date.date()


def inquire():
    questions = [
        inquirer.List('chart',
                      message="Which chart do you want data from?",
                      choices=['Hot 100', 'Pop Songs', 'Rock Songs', 'Hip-Hop/R&B Songs', 'Country Songs'],
                      carousel=True,
                      ),
    ]
    answers = inquirer.prompt(questions)
    return charts.get(answers['chart'])


if __name__ == '__main__':
    # Base url and dates for the Billboard Hot 100 chart, putting them into a
    # datetime object for easy addition and date manipulation

    billboard_url, base_year, base_month, base_day = inquire()

    curr_date = date(base_year, base_month, base_day)
    end_date = last_day()
    # Ask user for input to name the spreadsheet.
    sheetTitle = raw_input("Enter spreadsheet title: ").replace(" ", "_")
    sheetTitle = sheetTitle + ".csv"
    with open(sheetTitle, mode='w') as billboard_chart:
        charter = csv.writer(billboard_chart, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        charter.writerow(
            ["Artist", "Song", "Date", "Current Rank", "Last Weeks Position", "Weeks on Chart", "Peak Position"])
        while curr_date != end_date:
            scrape_site(charter, billboard_url, curr_date)
            print("Finished charting the week of: " + curr_date.isoformat())
            curr_date = date_increment(curr_date)
