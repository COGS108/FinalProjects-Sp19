from datetime import date, datetime, timedelta
import csv
import inquirer
from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from Queue import Queue
import threading
import time

session_lock = threading.Lock()
queue = Queue()
session = requests.Session()

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
    return [artist, song, dt.isoformat(), rank, last, peak, weeks]


def scrape_site(url, d, q):
    while True:
        for ind in range(len(d)):
            dt = d[ind]
            new_url = url + dt.isoformat()
            try:
                req = requests.get(new_url)
            except requests.exceptions.ConnectionError:
                session_lock.acquire()
                retry = Retry(connect=3, backoff_factor=0.5)
                adapter = HTTPAdapter(max_retries=retry)
                session.mount('http://', adapter)
                session.mount('https://', adapter)
                req = session.get(url)
                session_lock.release()
            soup = BeautifulSoup(req.text, "html.parser")
            songs = soup.find_all(class_="chart-list-item")
            hundred_list = [info(x, dt) for x in songs]
            q.put(hundred_list)


def write_results(q, title):
    while True:
        with open(title, mode='w') as billboard_chart:
            charter = csv.writer(billboard_chart, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            charter.writerow(
                ["Artist", "Song", "Date", "Current Rank", "Last Weeks Position", "Weeks on Chart", "Peak Position"])
            while True:
                row = q.get()
                charter.writerows(row)
                print("Finished charting the week of: " + (row[0])[2])


# def upload_worker(q, sheet_title):
#    while q.not_empty:
#        with open(sheet_title, mode='w') as billboard_chart:
#            charting = csv.writer(billboard_chart, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#            charting.writerow(q.get())


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

    while curr_date < end_date:
        dates = []
        for i in range(1000):
            if curr_date >= end_date:
                break
            dates.append(curr_date)
            curr_date = date_increment(curr_date)
        t = threading.Thread(target=scrape_site, args=(billboard_url, dates, queue))
        t.daemon = True
        t.start()
        print(curr_date)

    t = threading.Thread(target=write_results, args=(queue, sheetTitle))
    t.daemon = True
    t.start()
    time.sleep(5)
    queue.join()
