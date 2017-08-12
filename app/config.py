"""
@breif：read or write config
@author: vikadoo
@version: $id
"""
import json

from singleton import Singleton


class AppConfig(Singleton):
    """
    app config
    """
    def __init__(self):
        """
        init
        """
        super(AppConfig, self).__init__()
        self._configs = {}
        self._load_config()

    def _load_config(self):
        """
        load config file only once.
        """
        with open("config.json", 'r') as file:
            self._configs = json.load(file)

    def get_result_data_config(self):
        """
        get result data config
        """
        return self._configs.get("result_data", {})

    def get_task_data_config(self):
        """
        get task data config
        """
        return self._configs.get("task_data", {})

    def get_download_config(self):
        """
        get download config
        """
        return self._configs.get("download", {})
