"""
# --encoding=utf8 --
@brief: asynico download
@author: vikadoo
@version: $id
"""
import asyncio
import os
import urllib.request
from urllib.parse import quote


async def download_url(url):
    """
    @parame url
    """
    # response = urllib.request.urlretrieve(url, filename=None)
    try:
        response = urllib.request.urlopen(quote(url, safe='/:?='))
        file_name = os.path.basename(url)
        with open(file_name, 'wb') as file:
            while True:
                chunk = response.read(1024)
                if not chunk:
                    break
                file.write(chunk)

            print("Finished downloading {filename}".format(filename=file_name))
    except urllib.error.URLError as error:
        print(error)


def common_download(urls):
    """
    @breif: event loop
    @parame urls
    """
    event_loop = asyncio.get_event_loop()

    try:
        # create task
        coroutines = [download_url(url) for url in urls]
        event_loop.run_until_complete(asyncio.wait(coroutines))

    finally:
        event_loop.close()
