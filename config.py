import os


class Config:
    SCRAPING_DETAILS = {
        'url' : 'https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx',
        'tag': 'a',
        'element_attributes' : {
            'id' : 'ContentPlaceHolder1_btnhylZip'
        }
    }

    @staticmethod
    def get_config():
        if True:
            return DevConfig
        else:
            return GridConfig


class DevConfig(Config):
    isDev = True
    REDIS_CONNECTION_DETAILS = {
        'host' : 'redis-14243.c61.us-east-1-3.ec2.cloud.redislabs.com',
        'port' : 14243,
        'db' : 'alpha-db',
        'password' : 'ek6pm6EqhvAqjJRSLMP13bVj6EelqCp4'
    }
    # SCRAPING_DETAILS = {
    #     'url' : 'https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx',
    #     'tag': 'a',
    #     'element_attributes' : {
    #         'id' : 'ContentPlaceHolder1_btnhylZip'
    #     }
    # }
    ARCHIVE_DIRECTORY = os.getcwd()+os.sep+'bhav_copy_archives'


class GridConfig:
    REDIS_CONNECTION_DETAILS = {
        'host' : 'redis-14243.c61.us-east-1-3.ec2.cloud.redislabs.com',
        'port' : 14243,
        'db' : 'alpha-db',
        'password' : 'ek6pm6EqhvAqjJRSLMP13bVj6EelqCp4'
    }
    # SCRAPING_DETAILS = {
    #     'url' : 'https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx',
    #     'tag': 'a',
    #     'element_attributes' : {
    #         'id' : 'ContentPlaceHolder1_btnhylZip'
    #     }
    # }
    ARCHIVE_DIRECTORY = os.getcwd()+os.sep+'bhav_copy_archives'
