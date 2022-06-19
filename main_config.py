GET_DATA_UPDATE_INTERVAL = 60 # get_data sleep interval for While loop
ARCHIVE_DATA_FILENAME = 'data_archive.feater' # number of days available to analyze (backwards)
FRESH_DATA_FILENAME = 'fresh_data_dump.feather' # data_archive where last n=INCREMENT_DAYS_OFFSET days are updated
INITIAL_DAYS_OFFSET = 10 # archive data days offset
INCREMENT_DAYS_OFFSET = 3 # increment data days offset
DATA_HOST = 'http://149.126.169.223:4410' # data api host
