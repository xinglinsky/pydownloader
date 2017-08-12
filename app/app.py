"""
# --encoding=utf8--
@brief: app enter point
@author: vikadoo
@version: $id
"""
import asyncio
import sys

from PyQt5.QtCore import QCoreApplication

from download_scheduler import TaskDb
# from common_download import download_scheduler
from thunder_download import ThunderDownloader

TASKDB = TaskDb()
DOWNLOADER = ThunderDownloader()

def main():
    """
    You need this
    """
    app = QCoreApplication(sys.argv)
    TaskDb(app)

    # connect the downloader's signal and task-scheduler's slot
    DOWNLOADER.sigUrlDownloaded.connect(TASKDB.update_task_info)

    for url in TASKDB.get_task_urls():
        app_enter(url)

    # get task from database
    # event_loop = asyncio.get_event_loop()
    # try:
        # coroutine = [app_enter(url) for url in TASKDB.get_task_urls()]
        # event_loop.run_until_complete(asyncio.wait(coroutine))
    # finally:
        # event_loop.close()

    app.exec()

# async def app_enter(url):
def app_enter(url):
    """
    @parame url
    """
    if not url and not isinstance(url, str):
        return

    # download task
    if DOWNLOADER.download(url):
        # save to task db
        TASKDB.save_task_info(url, "")

if __name__ == '__main__':
    main()
