import requests
from bs4 import BeautifulSoup

from zipfile import ZipFile
from io import BytesIO, TextIOWrapper
from datetime import date
import csv
import json

from config import Config
from util.RedisUtil import RedisUtil
from util.file_archive_util import archive_file
conf = Config.get_config()


'''
    Method scrapes the bhav copy data from BSE's website, and populates the required data in redis
'''
def scrape_and_populate_data():
    file_bytes = None
    csv_file = None
    try:
        web_page_resp = do_get(conf.SCRAPING_DETAILS['url'])            # fetching the web page
        print('page fetched')

        ele = scrape_content(web_page_resp.content,
                             conf.SCRAPING_DETAILS['tag'],
                             conf.SCRAPING_DETAILS['element_attributes'])
        print(ele)

        [dd, mm, yyyy] = ele.contents[0].split(' ')[2].split('/')

        file_resp = do_get(ele['href'])                                 # fetching the zip content

        print('file fetched')
        zip_bytes = BytesIO(file_resp.content)

        zip = ZipFile(zip_bytes, 'r')
        file_name = zip.namelist()[0]                                   # file_name is the bhav_copy file
        csv_content = zip.read(file_name)                                   # read the contents of the csv file
        file_bytes = BytesIO(csv_content)
        print('zip contents read')

        csv_file = TextIOWrapper(file_bytes)
        _date = date(int(yyyy), int(mm), int(dd))
        populate_data(csv_file, _date)
        print('data populated to redis')

        archive_file(TextIOWrapper(BytesIO(zip.read(file_name))), _date)
        file_bytes.close()
        csv_file.close()
        print('file archived')
    except Exception as e:
        print('Unable to scrape and populate data for date: '+date.today().__str__())
        raise e
    finally:
        if file_bytes is not None:
            file_bytes.close()
        if csv_file is not None:
            csv_file.close()


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
        val = {name: json.dumps(obj)}
        RedisUtil.hm_set(date.__str__(), val)
