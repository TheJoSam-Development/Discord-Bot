"""An User Register used by the Bot"""

import csv
from os import path
#from modules import uuid_generator
import configparser
import logging
import json
from alive_progess import alive_bar

# WARNING! Do not change this if you dont know what you are doing!
PATH_CONFIG = './config/paths.cfg'
if path.exists(PATH_CONFIG):
    paths = configparser.ConfigParser()
    paths.read(PATH_CONFIG)
else: raise FileNotFoundError(f'File {PATH_CONFIG} not found! This is a big problem!')
CONFIG_PATH = paths.get(section='Config Files', option='user_register_config')
if path.exists(CONFIG_PATH):
    config = configparser.ConfigParser()
    config.read(paths.get(section='Config Files', option='user_register_config'))
else: raise FileNotFoundError(f'File {CONFIG_PATH} not found!')
LOGGER_CONFIG_FILE = paths.get(section='Log Paths', option='logger_cfg_file')

if path.exists(LOGGER_CONFIG_FILE):
    logging.config.dictConfig(
    json.loads(open(LOGGER_CONFIG_FILE, 'r').read()))
    logger = logging.getLogger(__name__)
else: raise FileNotFoundError(f'File {LOGGER_CONFIG_FILE} not found!')

class userRegister:
    def __init__(self, file_path: str):
        if config.get(section='Register', option='type') != 'CSV':
            raise ModuleNotFoundError('The Module you wanted is not available',
                                    name=config.get(section='Register', option='type'))
        if config.get(section='Register', option='type') == 'CSV':
            if not file_path.endswith(".csv"):
                raise IOError(f"File {file_path} is wrong type")
            self.file_path = file_path
            self.register_fields = [
                "user_id",
                "user_name",
                "internal_uuid",
                "join_date",
                "email",
            ]
            if path.exists(file_path):
                with open(file=file_path, mode="r", encoding="utf-8", newline="") as ur:
                    self.register_content = csv.DictReader(ur)
            else:
                with open(file=file_path, mode="w", encoding="utf-8", newline="") as ur:
                    self.register_writer = csv.DictWriter(ur, self.register_fields)
                    self.register_writer.writeheader()

            self.length = int(self._get_length())
    
    def add_user(self, discord_user):
        """Adds an user to register

        Args:
            discord_user (Discord Member object)
        """
        iid = uuid_generator.generate()
        user = {
            "user_name": discord_user.name,
            "user_id": discord_user.id,
            "internal_uuid": iid,
            "join_date": discord_user.join_date,
            "email": "NaN",
        }
        with open(
            file=self.file_path, mode="a+", encoding="utf-8", newline=""
        ) as user_register:
            register = csv.DictWriter(user_register, self.register_fields)
            register.writerow(user)
        self.length += 1
    
    def get_user_by_id(self, user_id: str):
        """
        Returns an specified user by the Discord User ID (DUID)

        Args:
            user_id (str): Discord User ID
        """
        if not config.getboolean("Functions", "get_user-duid"):
            raise ModuleNotFoundError(
                "Function get_user_by_id is diabled (if this is not desired activate it in the config)"
            )
        with open(
            file=self.file_path, mode="r+", encoding="utf-8", newline=""
        ) as user_register:
            reader = csv.DictReader(user_register)
            output = None
            row_id = 0
            with alive_bar(
                self.length,
                title='Searching',
                length=30,
                spinner_length=5
            ) as progress_bar:
                # pylint: disable=not-callable
                for row in reader:
                    progress_bar.text(f'Processing row {row_id}')
                    row_id += 1
                    if row["user_id"] == user_id:
                        output = row
                    progress_bar()
            if output is None:
                raise IndexError(f'No User found with id: {user_id}')
            return output

    def delete_user(self, user_id = None, tuuid = None):
        """
        Deletes an User using an DUID or TUUID
        
        **WARNING!** Only 1 search algorythm is usable when bove is used an Excetion is raised
        
        Args:
            user_id (str) [None]: if set activates DUID search
            tuuid (str) [None]: if set activates TUUID search
        """
        raise NotImplementedError('This feature must be done manually!')

    def _get_length(self):
        """
        **[INTERNAL FUNCTION]**

        Returns the lenght of the current User Register
        used mainly by search function to create an out of index check
        """
        if not config.getboolean("Functions", "get_length"):
            raise ModuleNotFoundError(
                "Function get_length is diabled (if this is not desired activate it in the config)"
            )
        length = 0
        with open(
            file=self.file_path, mode="r+", encoding="utf-8", newline=""
        ) as user_register:
            # pylint: disable=unused-variable
            reader = csv.DictReader(user_register)
            for row in reader:
                length += 1
        return length

    def _check_for_id(self, user_id: str):
        """
        **[INTERNAL FUNCTION]**

        Searches for an user by ID
        this is helpful when checking for duplicates
        as users can have the same name but not the same id
        """
        if not config.getboolean("Functions", "check_for_id"):
            raise ModuleNotFoundError(
                "Function check_for_id is diabled (if this is not desired activate it in the config)"
            )
        with open(
            file=self.file_path, mode="r+", encoding="utf-8", newline=""
        ) as user_register:
            reader = csv.DictReader(user_register)
            row_id = 0
            for row in reader:
                row_id += 1
                if row["user_id"] == user_id:
                    return row
                if row_id > self.length:
                    raise IndexError(
                        f"user id {user_id} was not found in user register"
                    )
