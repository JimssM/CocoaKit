#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import configparser
import os
import traceback

# Get the directory path of the current script
current_path = os.path.dirname(__file__)


class Config:
    def __init__(self, path):
        """
        Initialize the configuration class.
        :param path: Path to the configuration file.
        """
        self.path = path
        self.config = configparser.ConfigParser()
        self.config.read(path, encoding='gbk')

    def get_value(self, section, key):
        """
        Retrieve the value of a specific key under a given section.
        :param section: Section name in the configuration file.
        :param key: Key name under the specified section.
        :return: The value associated with the key, or an empty string if retrieval fails.
        """
        try:
            return self.config.get(section, key)
        except:
            print(self.path)
            traceback.print_exc()
            return ""

    def get_items(self, section):
        """
        Retrieve all key-value pairs under a specific section.
        :param section: Section name in the configuration file.
        :return: A list of key-value pairs in the format [(key1, value1), (key2, value2)].
        """
        return self.config.items(section)

    def add_section(self, section):
        """
        Add a new section to the configuration file.
        :param section: Name of the section to add.
        """
        try:
            self.config.add_section(section)
        except Exception as E:
            # Ignore exception if the section already exists
            pass

    def set(self, section, key, value):
        """
        Set a key-value pair under a specified section.
        :param section: Section name in the configuration file.
        :param key: Key name.
        :param value: Value to be associated with the key.
        """
        self.config.set(section, key, value)

    def write(self):
        """
        Save the configuration content to the file.
        """
        with open(self.path, "w") as fp:
            self.config.write(fp)
