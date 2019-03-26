class Config:
    isDev = True

    @staticmethod
    def get_config():
        if Config.isDev:
            return DevConfig
        else:
            return GridConfig

class DevConfig:
    REDIS_CONNECTION_DETAILS = {
        'host' : 'localhost',
        'port' : 6379,
        'db' : 0
    }
    SCRAPING_DETAILS = {
        'url' : 'https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx',
        'element_attributes' : {
            'id' : 'ContentPlaceHolder1_btnhylZip'
        }
    }
    ARCHIVE_DIRECTORY = './bhav_copy_archives'

class GridConfig:
    REDIS_CONNECTION_DETAILS = {
        'host' : 'localhost',
        'port' : 6379,
        'db' : 0
    }
    SCRAPING_DETAILS = {
        'url' : 'https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx',
        'element_attributes' : {
            'id' : 'ContentPlaceHolder1_btnhylZip'
        }
    }
    ARCHIVE_DIRECTORY = './bhav_copy_archives'