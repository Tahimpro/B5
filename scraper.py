import requests
from bs4 import BeautifulSoup
import re
from info import HEADERS

BASE_URL = "https://skymovieshd.video/"
HOWBLOGS_PATTERN = re.compile(r'https://howblogs\.xyz/\S+')

def get_latest_movies():
    """Scrapes the latest uploaded movies from skymovieshd.video"""
    response = requests.get(BASE_URL, headers=HEADERS)
    if response.status_code != 200:
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    movie_links = [a['href'] for a in soup.find_all('a', href=True) if '/movie/' in a['href']]
    return list(set(movie_links))

def get_howblogs_link(movie_url):
    """Extracts howblogs.xyz link from the movie page"""
    response = requests.get(movie_url, headers=HEADERS)
    if response.status_code != 200:
        return None
    
    matches = HOWBLOGS_PATTERN.findall(response.text)
    return matches[0] if matches else None

def get_hubdrive_link(howblogs_url):
    """Finds hubdrive.dad link from howblogs.xyz page"""
    response = requests.get(howblogs_url, headers=HEADERS)
    if response.status_code != 200:
        return None
    
    soup = BeautifulSoup(response.text, "html.parser")
    for a in soup.find_all("a", href=True):
        if "hubdrive.dad" in a["href"]:
            return a["href"]
    return None

def get_final_download_link(hubdrive_url):
    """Extracts the final download link from hubdrive.dad"""
    response = requests.get(hubdrive_url, headers=HEADERS)
    if response.status_code != 200:
        return None
    
    soup = BeautifulSoup(response.text, "html.parser")
    for a in soup.find_all("a", href=True):
        if "Download Here" in a.text:
            return a["href"]
    return None
