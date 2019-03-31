import os


class Config:
    isDev = False
    SCRAPING_DETAILS = {
        'url' : 'https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx',
        'tag': 'a',
        'element_attributes' : {
            'id' : 'ContentPlaceHolder1_btnhylZip'
        }
    }
    POPULATE_DATA_AUTH_TOKEN = 'ksnwo3wh7edwihdiq23&*&^Yi7'

    @staticmethod
    def get_config():
        if False:                    #TODO check if the config is for dev or grid
            return DevConfig
        else:
            return GridConfig


class DevConfig(Config):
    isDev = True
    # REDIS_CONNECTION_DETAILS = {
    #     'host' : 'redis-14243.c61.us-east-1-3.ec2.cloud.redislabs.com',
    #     'port' : 14243,
    #     'password' : 'ek6pm6EqhvAqjJRSLMP13bVj6EelqCp4'
    # }
    REDIS_CONNECTION_DETAILS = {
        'host': 'localhost',
        'port': 6379,
        'db': 0
    }
    ARCHIVE_DIRECTORY = os.getcwd()+os.sep+'bhav_copy_archives'


class GridConfig:
    REDIS_CONNECTION_DETAILS = {
        'host': 'redis-14243.c61.us-east-1-3.ec2.cloud.redislabs.com',
        'port': 14243,
        'password': 'ek6pm6EqhvAqjJRSLMP13bVj6EelqCp4'
    }
    ARCHIVE_DIRECTORY = os.getcwd()+os.sep+'bhav_copy_archives'
