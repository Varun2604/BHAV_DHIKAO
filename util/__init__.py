import requests
from bs4 import BeautifulSoup

from zipfile import ZipFile
from io import BytesIO, TextIOWrapper, BufferedIOBase
from datetime import date
import csv
import json

from config import Config
from util.RedisConnection import RedisConnection

conf = Config.get_config()


'''
    Method scrapes the bhav copy data from BSE's website, and populates the required data in redis
'''
def scrape_and_populate_data():
    try:
        web_page_resp = do_get(conf.SCRAPING_DETAILS['url'])            # fetching the web page
        ele = scrape_content(web_page_resp.content,
                             conf.SCRAPING_DETAILS['tag'],
                             conf.SCRAPING_DETAILS['element_attributes'])
        [dd, mm, yyyy] = ele.contents[0].split(' ')[2].split('/')

        file_resp = do_get(ele['href'])                                 # fetching the zip content
        zip_bytes = BytesIO(file_resp.content)

        zip = ZipFile(zip_bytes, 'r')
        file_name = zip.namelist()[0]                                   # file_name is the bhav_copy file
        content = zip.read(file_name)                                   # read the contents of the csv file
        file_bytes = BufferedIOBase(content)

        csv_file = TextIOWrapper(file_bytes)
        _date = date(yyyy, mm, dd)
        populate_data(csv_file, _date)

        file_bytes.close()
        arc_file = open(_date.__str__()+'.CSV', 'w')
        arc_file.write(conf.ARCHIVE_DIRECTORY)
    except:
        print('Unable to scrape and populate data for date: '+date.today().__str__())


'''
    Returns response for the given url
    Does not do exception handling
'''
def do_get(url):
    return requests.get(url)


'''
    Scrapes the given content for the tag and the attributes with bs4
'''
def scrape_content(content, tag, attributes):
    soup = BeautifulSoup(content, 'html5lib')
    return soup.find(tag, attrs=attributes)

'''
    given the CSV file and the date, the method populates the required data in Redis
'''
def populate_data(csv_file, date):
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        name = row['SC_NAME'].strip()
        obj = {
            'code': row['SC_CODE'].strip(),
            'name': row['SC_NAME'].strip(),
            'open': row['OPEN'].strip(),
            'high': row['HIGH'].strip(),
            'low': row['LOW'].strip(),
            'close': row['CLOSE'].strip()
        }
        val = {
            [name]: json.dumps(obj)
        }
        RedisConnection.hm_set(date.__str__(), val)
