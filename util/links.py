import requests
from bs4 import BeautifulSoup
from util.config import retryBackoff, reqSleep, baseURL
import time

def extractLinks(url):
    time.sleep(reqSleep)
    newLinks = []
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    try:
        page = requests.get(url, headers=headers)
    except:
        try:
            time.sleep(retryBackoff)
            page = requests.get(url, headers=headers)
        except:
            return []

    soup = BeautifulSoup(page.text, 'lxml')
    mylinks = soup.findAll("a", { "class" : "Directory-listLink" })
    for i in range(len(mylinks)):
        link = mylinks[i]
        newLink = link['href']
        ending = newLink.split('/')[-1].split('.')[0]
        newLinks.append(baseURL + '/' + ending)
    
    return newLinks

def extractCityLinks(url):
    time.sleep(reqSleep)
    newLinksStore = []
    newLinksCity = []
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    try:
        page = requests.get(url, headers=headers)
    except:
        try:
            time.sleep(retryBackoff)
            page = requests.get(url, headers=headers)
        except:
            return [], []

    soup = BeautifulSoup(page.text, 'lxml')
    mylinks = soup.findAll("a", { "class" : "Directory-listLink" })
    for i in range(len(mylinks)):
        link = mylinks[i]
        newLink = link['href']
        if len(newLink.split('/')) == 2:
            newLinksCity.append(baseURL + '/' + newLink)
        else:
            newLinksStore.append(baseURL + '/' + newLink)
    
    return newLinksCity, newLinksStore

def extractStoreLinks(url):
    time.sleep(reqSleep)
    newLinks = []
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    try:
        page = requests.get(url, headers=headers)
    except:
        try:
            time.sleep(retryBackoff)
            page = requests.get(url, headers=headers)
        except:
            return []
    soup = BeautifulSoup(page.text, 'lxml')
    mylinks = soup.findAll("a", { "class" : "Teaser-titleLink" })
    for i in range(len(mylinks)):
        link = mylinks[i]
        newLink = link['href']
        ending = newLink.split('/')[-1].split('.')[0]
        newLinks.append(url + '/' + ending)
    
    return newLinks

def extractStoreInfo(url):
    time.sleep(reqSleep)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    try:
        page = requests.get(url, headers=headers)
    except:
        try:
            time.sleep(retryBackoff)
            page = requests.get(url, headers=headers)
        except:
            return []
    soup = BeautifulSoup(page.text, 'lxml')
    storeNum = 'null'
    city = url.split('/')[-2]
    state = url.split('/')[-3]
    try:
        name = soup.find("span", { "class" : "Hero-locationGeo" }).text
    except:
        name = ''

    try:
        phoneNumber = soup.find("a", { "class" : "Phone-link" })['href'].split('+')[-1]
    except:
        phoneNumber = ''

    try:
        address = soup.find("address", { "class" : "Core-address" }).text.split('United States')[0]
    except:
        address = ''

    try:
        latitude = soup.find("meta", { "itemprop" : "latitude" })['content']
    except:
        latitude = ''

    try:
        longitude = soup.find("meta", { "itemprop" : "longitude" })['content']
    except:
        longitude = ''

    return [name, storeNum, phoneNumber, address, url, longitude, latitude, city, state]