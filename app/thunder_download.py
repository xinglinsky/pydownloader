"""
@breif: thunder download
"""
import os.path

from PyQt5.QtCore import (QFileSystemWatcher, QObject, QProcess, QUrl,
                          pyqtSignal)

from config import AppConfig


class ThunderDownloader(QObject):
    """
    a class for download using thunder on windows
    """
    WIN_THUNDER_EXE = "Thunder.exe"
    WIN_THUNDER_TASK_EXE = "ThunderNewTask.exe"

    # emit when the url is downloaded
    # parame: url(str), path(str)
    sigUrlDownloaded = pyqtSignal(str, str)

    def __init__(self, *args):
        super(ThunderDownloader, self).__init__(*args)
        self._thunder_path = AppConfig().get_download_config().get("thunder_path", "")
        self._save_path = AppConfig().get_download_config().get("save_path", "")
        self._thunder_process = None
        self._thunder_task_process = None
        self._download_urls = []
        self._file_watcher = QFileSystemWatcher(self)
        self._file_watcher.addPath(self._save_path)
        self._file_watcher.directoryChanged.connect(self._on_file_dir_changed)

    def thunder_exe_download(self, url):
        """
        execute the download task by progame installed in windows system
        @parame: url
        """
        if self._thunder_process is None:
            self._thunder_process = QProcess(self)
            self._thunder_process.start(
                os.path.join(
                    self._thunder_path, ThunderDownloader.WIN_THUNDER_EXE), [
                        "-silent", "-noshowfloatpanel", "-noshownewtaskdlg",
                        "-StartFrom:XLDownloadClient",
                        "-StartType:XLDownloadClient",
                        "-ClientProcess:ThunderNewTask.exe"
                    ])

        if self._thunder_process.waitForStarted(60000):
            self.thunder_add_task(url)
        else:
            print("failt to start thunder process %s" % url)

    def thunder_add_task(self, url):
        """
        @parame url
        """
        QProcess.execute(os.path.join(self._thunder_path, ThunderDownloader.WIN_THUNDER_TASK_EXE), [url])
        print("start add task %s" % url)

    def thunder_sdk_download(self, url):
        """
        TODO: download url by sdk interface
        """
        pass

    # def download(self, urls):
    #     """
    #     download scheduler
    #     """
    #     event_loop = asyncio.get_event_loop()

    #     try:
    #         coroutine = [self.thunder_exe_download(url) for url in urls]
    #         event_loop.run_until_complete(asyncio.wait(coroutine))
    #     finally:
    #         event_loop.close()

    def _on_file_dir_changed(self, path):
        """
        @parame path
        """
        files = os.listdir(path)
        for url in iter(self._download_urls):
            file_name = os.path.basename(url)
            if file_name in files:
                self.sigUrlDownloaded.emit(url, os.path.join(path, file_name))
                self._download_urls.remove(url)
                print("file(%s) is downloaded." % file_name)

    def download(self, url):
        """
        download scheduler
        """
        # check whether file is existed
        file_name = os.path.basename(url)
        if file_name in os.listdir(self._save_path):
            return False

        try:
            self.thunder_exe_download(url)
        except:
            print("some error happend when download %s" % url)
            return False
        else:
            self._download_urls.append(url)
            return True
