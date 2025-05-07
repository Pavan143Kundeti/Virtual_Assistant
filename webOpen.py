import webbrowser
import requests
from bs4 import BeautifulSoup
import threading
import smtplib
import urllib.request
import os
from pytube import YouTube
from youtubesearchpython import VideosSearch


# to download yt video
def latestNews(news=2):
    URL = 'https://indianexpress.com/latest-news/'
    result = requests.get(URL)
    src = result.content

    soup = BeautifulSoup(src, 'html.parser')

    headlineLinks = []
    headlines = []

    divs = soup.find_all('div', {'class': 'title'})

    count = 0
    for div in divs:
        count += 1
        if count > news:
            break
        a_tag = div.find('a')
        headlineLinks.append(a_tag.attrs['href'])
        headlines.append(a_tag.text)

    return headlines


def openWebsite(url='https://www.google.com/'):
    webbrowser.open(url)
import subprocess


def openWebsiteByName(query):

# Get the URL from the user
    query = query.replace('open', '').replace('website', '').strip()
    url=query+'.com'
    subprocess.run(["start", "chrome", url], shell=True)  # Replace 'chrome' with your browser name



def handleQuery(query):
    URL = "https://www.google.co.in/search?q=" + query
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53'
    }
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    result = soup.find(class_='Z0LcW').get_text()
    return result

from youtubesearchpython import VideosSearch
import webbrowser

def youtube(query):
    # Clean up the query to remove unnecessary words
    query = query.replace('play', '').replace('on youtube', '').replace('youtube', '').strip()

    print(f"Searching for video: {query}")

    # Search for the video using youtubesearchpython
    videosSearch = VideosSearch(query, limit=1)
    results = videosSearch.result()['result']

    if results:
        # Get the YouTube URL from the search results
        video_url = 'https://www.youtube.com/watch?v=' + results[0]['id']
        print(f"Found video: {video_url}")  # Debugging the video URL
        
        try:
            # Open the video in the default browser
            webbrowser.open(video_url)
            print("Opening video in browser...")
            return "Enjoy the video!"
        except Exception as e:
            print(f"Error opening video: {e}")
            return "Failed to open the video."
    else:
        print("No video found for the query.")
        return "No video found."





# for downloading yt video
def get_itag(yt=None):
    tag_audio = list(yt.streams.filter(only_audio=True))
    tag_video = list(yt.streams.filter(file_extension='mp4'))

    audio_itag = {}
    video_itag = {}
    video_itag_nosound = {}
    all_res = []

    i = 1
    for stream in tag_audio:
        stream = f'{stream}'
        stream = stream.split(' ')
        itag, abr = stream[1], stream[3]
        itag_num = itag.split('"')[1]
        abr_num = abr.split('"')[1]

        audio_itag[i] = {abr_num: itag_num}
        i += 1

    j = 1
    for stream in tag_video:
        stream = f'{stream}'
        stream = stream.split(' ')
        itag, res, fps, pro = stream[1], stream[3], stream[4], stream[-2]

        if 'True' in pro:
            if 'res' in res:
                itag_num = itag.split('"')[1]
                res_num = res.split('"')[1]
                fps_num = fps.split('"')[1]

                video_itag[j] = {f'{res_num}-{fps_num}': itag_num}
                j += 1
        else:
            if 'res' in res:
                if res not in all_res:
                    all_res.append(res)
                    itag_num = itag.split('"')[1]
                    res_num = res.split('"')[1]
                    fps_num = fps.split('"')[1]

                    video_itag_nosound[j] = {f'no-sound-{res_num}-{fps_num}': itag_num}
                    j += 1

    return audio_itag, video_itag, video_itag_nosound


def download_by_itag(PATH, itag=None, type='mp4', yt=None, title=None):
    stream = yt.streams.get_by_itag(itag)
    if type == 'mp3':
        stream.download(PATH, f'audio.{type}')
    else:
        stream.download(PATH, f'video.{type}')


def downloadVideo(query):
    query = query.replace('download', '').replace('from youtube', '').replace('from yt', '').strip()

    videosSearch = VideosSearch(query, limit=1)
    results = videosSearch.result()['result']
    print("Finished searching!")

    URL = 'https://www.youtube.com/watch?v=' + results[0]['id']

    yt = YouTube(URL)

    title = yt.title
    print(f'!Downloading: {title}')
    audio_itag, video_itag, video_itag_nosound = get_itag(yt)

    qt = 2  # Resolution selection (720p currently)
    if qt <= len(video_itag):
        itag = int(list(video_itag[qt].values())[0])
    else:
        itag = int(list(video_itag_nosound[qt].values())[0])

    download_folder = os.path.join(os.environ['USERPROFILE'], 'Downloads')
    PATH = os.path.join(download_folder, title)

    print(f'Downloading video: {title}')
    download_by_itag(PATH, itag, 'mp4', yt, 'video')

    print('Download successful! Check your "Downloads" folder.')


def googleSearch(query):
    if 'image' in query:
        query += "&tbm=isch"

    query = query.replace('images', '').replace('image', '').replace('search', '').replace('show', '').replace('on google', '')

    webbrowser.open(f"https://www.google.com/search?q={query}")
    return "Here you go..."

import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import urllib.request

def downloadImage(query, n=10):
    query = query.replace('of', '').replace('images', '').replace('image', '').replace('download', '')
    URL = f"https://www.google.com/search?tbm=isch&q={query}"

    # Set up Selenium WebDriver
    options = Options()
    options.headless = True  # Run in headless mode (no browser window)
    driver = webdriver.Chrome(options=options)

    driver.get(URL)
    time.sleep(3)  # Let the page load

    # Scroll the page to load more images (optional)
    for _ in range(3):  # Scroll 3 times (adjust if needed)
        driver.execute_script("window.scrollBy(0,1000);")
        time.sleep(2)

    # Find image elements
    imgTags = driver.find_elements(By.TAG_NAME, 'img')

    if not os.path.exists('Downloads'):
        os.mkdir('Downloads')

    count = 0
    for i in imgTags:
        if count == n:
            break
        try:
            img_url = i.get_attribute('src')
            if img_url:
                urllib.request.urlretrieve(img_url, f'Downloads/{count}.jpg')
                count += 1
        except Exception as e:
            print(f"Error downloading image {count}: {e}")

    print(f'Downloaded {count} images')
    driver.quit()  # Close the browser


if __name__ == "__main__":
    # Uncomment the functions you want to test:
    # downloadImage('download images of cat')
    # googleSearch('search tom cruise on google')
    # youtube("play gangnam style on youtube")
    # openWebsiteByName('open apple website')
    # openWebsite()
    downloadVideo('download rainy day short 30 sec animation video')
