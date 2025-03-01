# general configuration for the program
# - directory to store information like hiscore
# - directory to store information per user (appdata)
# - username

import os
import getpass

class Config:
    DATAPATH = 'c:/programdata/connectlog2'

    @staticmethod
    def make_user_datapath() -> None:
        path = Config.get_user_datapath()
        if os.path.exists(path) and not os.path.isdir(path):
            os.remove(path)
        if not os.path.exists(path):
            os.mkdir(path, 555)

    @staticmethod
    def make_datapath() -> None:
        if os.path.exists(Config.DATAPATH) and not os.path.isdir(Config.DATAPATH):
            os.remove(Config.DATAPATH)
        if not os.path.exists(Config.DATAPATH):
            os.mkdir(Config.DATAPATH, 555)
    @staticmethod
    def get_user_datapath() -> str:
        return os.path.join(os.environ['USERPROFILE'], 'appdata', 'roaming', 'connectlog2')

    @staticmethod
    def get_datapath() -> str:
        return Config.DATAPATH

    @staticmethod
    def get_user() -> str:
        return getpass.getuser()





