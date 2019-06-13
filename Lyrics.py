# get the lyrics from the url
import requests
from bs4 import BeautifulSoup
import re

def GetLyricsFromURL(url):
  req = requests.get(url)
  slash_pos = url.rfind('/') #find the last position of '/'
  key = url[slash_pos+1:]

  # find lyrics <a> tags that have those key
  soup = BeautifulSoup(req.text, "html.parser")
  lyr = soup.find_all('a', {'href': re.compile(key)})
  lyrics = "".join([l.get_text() for l in lyr])
  return lyrics