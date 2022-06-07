from data_prep.data_scheduling import check_archive_update_time, remove_archive
from get_data import update_data
import index


if __name__ == '__main__':
    index.app.run_server(debug=True)
