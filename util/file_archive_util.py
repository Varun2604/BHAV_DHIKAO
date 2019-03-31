import os

from config import Config
conf = Config.get_config()


'''
    Method the given readable file in the archive directory
'''
def archive_file(readable_content, date):
    #TODO archive the files in a DFS.
    # if conf.isDev:
    arc_file = None
    try:
        arc_file = open(conf.ARCHIVE_DIRECTORY + os.sep + date.__str__() + '.CSV', 'w')
        arc_file.write(readable_content.read())
    except Exception as e:
        print('Error while archiving file for date'+date.__str__())
        raise e
    finally:
        arc_file.close()

