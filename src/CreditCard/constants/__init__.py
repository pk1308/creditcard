import os 
from datetime import datetime


def get_current_time_stamp():
    return f"{datetime.now().strftime('%Y%m%d%H%M%S')}"


ROOT_DIR = os.getcwd()  # to get current working directory
CURRENT_TIME_STAMP = get_current_time_stamp()
# config constants
CONFIG_DIR = os.path.join(ROOT_DIR, 'configs')
CONFIG_FILE_NAME = "config.yaml"
CONFIG_FILE_PATH = os.path.join(CONFIG_DIR, CONFIG_FILE_NAME)