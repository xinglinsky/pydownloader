"""
# --encoding=utf8--
@brief: get task to do
@author: vikadoo
@version: $date
"""
import hashlib
import json

import pymysql

from contextlib import closing
from config import AppConfig
from PyQt5.QtCore import pyqtSlot, QObject


class TaskDb(QObject):
    """
    control db for task, to save task information , get task urls and so on.
    """
    def __init__(self, *args):
        """
        initilized data
        """
        super(TaskDb, self).__init__(*args)
        self._taskdb_config = AppConfig().get_task_data_config()
        self._resultdb_config = AppConfig().get_result_data_config()

    @staticmethod
    def get_task_id(url):
        """
        @parame url
        @return md5 str
        """
        md5 = hashlib.md5()
        md5.update(url.encode() if isinstance(url, str) else url)
        return md5.hexdigest()

    def get_task_urls(self):
        """
        get 10 records once abourt task urls from database
        @return urls
        """
        # get the count of task
        task_data = ()
        try:
            task_db_con = pymysql.connect(**self._taskdb_config)
            with task_db_con.cursor() as task_cursor:
                task_cursor.execute('SELECT DISTINCT url FROM mv')
                task_data = task_cursor.fetchall()
        finally:
            task_db_con.close()

        try:
            result_db_con = pymysql.connect(**self._resultdb_config)
            with result_db_con.cursor() as result_cursor:
                # get all result
                result_cursor.execute('SELECT DISTINCT result FROM dytt8')
                data = result_cursor.fetchall()

                # compare task count with result count
                if len(task_data) < len(data):
                    return map(lambda row_item: json.loads(row_item[0]).get("mv_url"), data)
                return iter(task_data)
        finally:
            result_db_con.close()

    def save_task_info(self, url, path):
        """
        save task information to database
        @parame url
        @parame path
        """
        try:
            db_connect = pymysql.connect(**self._taskdb_config)
            with db_connect.cursor() as cursor: 
                task_id = self.get_task_id(url)
                cursor.execute("INSERT INTO mv (taskid, url, localpath) VALUES ('%s', '%s', '%s')" % (task_id, url, path))
            db_connect.commit()
        except:
            db_connect.rollback()
            print("Fail to save task info, url=%s" % url)
        else:
            print("Success saving task info, url=%s" % url)
        finally:
            db_connect.close()

    @pyqtSlot(str, str)
    def update_task_info(self, url, path):
        """
        update task information to database
        @parame url
        @parame path
        """
        try:
            db_connect = pymysql.connect(**self._taskdb_config)
            with db_connect.cursor() as cursor:
                task_id = self.get_task_id(url)
                cursor.execute("UPDATE mv SET localpath = '%s' WHERE taskid = '%s'" % (path, task_id))
                db_connect.commit()
        except:
            db_connect.rollback()
            print("Fail updating task information, url=%s, path=%s" % (url, path))
        else:
            print("Success updating task information, url=%s, path=%s" % (url, path))
        finally:
            db_connect.close()
