from enum import Enum

token = '1509933539:AAEQsZTMQtvU4un3u5wavnYCMPUIi6eUo9s'
db_file = 'database.vdb'

user_age = 'user_age_data.vdb'
user_name = 'user_name_data.vdb'
user_sex = 'user_sex_data.vdb'

class States(Enum):
    S_START = "0"
    S_ENTER_NAME = "1"
    S_ENTER_AGE = "2"
    S_ENTER_SEX = "3"
    S_MENU = "4"
    S_NEW_NAME = "5"
    S_NEW_AGE = "6"
    S_NEW_SEX = "7"
    S_SETTING = "8"