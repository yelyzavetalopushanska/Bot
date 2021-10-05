from vedis import Vedis
import config

def get_user_data(user_id, data):
    with Vedis(data) as db:
        try:
            return db[user_id].decode()
        except KeyError:
            return config.States.S_START.value

def set_user_data(user_id, data, value):
    with Vedis(data) as db:
        try:
            db[user_id] = value
        except:
            return False