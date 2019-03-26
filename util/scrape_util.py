import requests
import zipfile
import io
from bs4 import BeautifulSoup
import csv

from config import  Config
conf = Config.get_config()

def scrape_bhav_copy():
    r = requests.get(conf.SCRAPING_DETAILS['url'])
    soup = BeautifulSoup(r.content, 'html5lib')
    a = soup.find('a', attrs = {'id':'ContentPlaceHolder1_btnhylZip'})
    # date = a.contents[0]
    [dd, mm, yyyy] = a.contents[0].split(' ')[2].split('/')
    file_res = requests.get(a['href'])          #TODO handle error cases
    f = io.BytesIO(file_res.content)
    zip = zipfile.ZipFile(f, 'r')
    file_name = zip.namelist()[0]               #file_name is the bhav_copy file
    content = zip.read(file_name)                         # read the contents of the csv file
    b = io.BytesIO(content)
    t = io.TextIOWrapper(b)
    csv_reader = csv.DictReader(f)
    for row in csv_reader:
        name = row['SC_NAME'].strip()


