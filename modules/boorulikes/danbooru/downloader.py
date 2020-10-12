# danbooru downloader
import time

import requests

from modules.defaults import downloader


class Downloader(downloader.Downloader):
    def __init__(self, config):
        super().__init__(config)
        self._session = requests.Session()
        headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                   "Accept-Encoding": "gzip, deflate",
                   "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                   "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:79.0) Gecko/20100101 Firefox/79.0"}
        self._session.headers = headers

    def request(self, journal, reporter):
        while journal.following_urls:
            url = self._schedule_next_url(journal)
            try:
                journal.console.write("sending request: %s" % url)
                resp = self._session.get(url)
                if resp.ok:
                    journal.console.write("\tResponse: 200")
                    journal.done_with_url(url, resp)
                else:
                    journal.console.write("\tResponse: %s" % resp.status_code)
                    journal.failed_urls[url] = resp.status_code
                    reporter.post(failed_urls=(url, resp.status_code))
            except Exception as e:
                # encountered TimeoutError, urllib3.exceptions.ProtocolError, requests.exceptions.ConnectionError
                journal.console.write("\tfailed: %s" % e.__str__())
                journal.failed_urls.append(url)
                reporter.post(failed_urls=(url, e))

            time.sleep(self._config.interval())

        journal.following_urls.clear()

    def _schedule_next_url(self, journal):
        # for danbooru downloader, the client may want to get picture file as soon as possible.
        for url in journal.following_urls:
            if self._is_pic_url(url):
                journal.following_urls.remove(url)
                return url
        else:
            return journal.following_urls.pop(0)

    @staticmethod
    def _is_pic_url(url):
        if url[url.rfind('/')+1:].startswith('__'):
            return True
        else:
            return False
