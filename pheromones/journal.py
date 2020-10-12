# Journal carries information about a single task.
# any config in Journal would override default config.
import random


class Console:
    def __init__(self, mode):
        self.mode = mode

    def write(self, obj):
        if self.mode == "Drone":
            print(obj)


class Journal:
    def __init__(self,
                 *keywords,
                 filters=None,
                 pool_mode=False,
                 pool_name=None,
                 save_path=None,
                 save_pattern=None,
                 interval=None,
                 console_mode="Drone"):
        self.main_keywords = []
        self.other_keywords = []
        self._set_keywords(*keywords)

        self._filter = filters  # a expressions controls filtering.

        self.pool_mode = pool_mode
        self.pool_name = pool_name

        # these three options would override default behavior in config file.
        self.save_path = save_path
        self.save_pattern = save_pattern
        self.interval = interval

        self.following_urls = list()  # urls to request
        self.done_urls = list()  # to avoid repeated get

        self.failed_urls = dict()  # timeout or other request excepted urls
        # {'url': exception}

        self.max_pending = 1000  # max following urls count.

        self.url_responses = {}  # 'url': response object
        # once done with the response, should remove item.

        self.content_to_save = {}  # "url": content

        self.force_task_finished = False

        self.console = Console(console_mode)

    def _set_keywords(self, *args):
        if len(args) < 2:
            self.main_keywords = list(args)
        else:
            self.main_keywords = list(args[:2])
            for kw in args[2:]:
                self.other_keywords.append(kw)

    @property
    def task_finished(self):
        # the condition of stop doing the job
        if self.force_task_finished:  # set True to force stop the task.
            return True
        if self.following_urls \
                or self.content_to_save \
                or self.url_responses:
            return False
        else:
            return True

    def has_url(self, url):
        if url in self.following_urls:
            return True
        if url in self.done_urls:
            return True
        if url in self.content_to_save:
            return True
        if url in self.url_responses:
            return True
        if url in self.failed_urls:
            return True
        return False

    def new_urls(self, *urls):
        for url in urls:
            if not self.has_url(url) \
                    and (len(self.following_urls) < self.max_pending):
                self.following_urls.append(url)

    def done_with_url(self, url, response):
        self.done_urls.append(url)
        self.url_responses[url] = response

    def redo_url(self, url):
        if url in self.done_urls:
            self.done_urls.remove(url)
        self.new_urls(url)
