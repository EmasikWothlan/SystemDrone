from modules.defaults import reporter


class Reporter(reporter.Reporter):
    def __init__(self, config):
        super().__init__(config)
        self._event_value_dict['task_name'] = ''
        self._event_value_dict['max_query_pages'] = 0
        self._event_value_dict['extracted_query_pages'] = 0
        self._event_value_dict['total_posts'] = 0
        self._event_value_dict['tag_of_pics'] = {}
        self._event_value_dict['keywords'] = []
        self.task_name = None
        self.max_query_pages = 1
        self.extracted_query_pages = 0
        self.pic_saved = 0
        self.pic_already_exist = 0
        self.total_posts = 0
        self.tag_of_pics = {}
        self.keywords = []
        self.failed_urls = {}  # {'url': exception}

    def post(self, *nouse_args, method='default', **event_value):
        super(Reporter, self).post(*nouse_args, method='default', **event_value)

        # there must another way to get rid of this ugly stuff
        if "task_name" in event_value:
            self.task_name = event_value.pop("task_name")
            self._event_value_dict["task_name"] = self.task_name
        if "max_query_pages" in event_value:
            self.max_query_pages = event_value.pop("max_query_pages")
            self._event_value_dict["max_query_page"] = self.max_query_pages
        if "extracted_query_pages" in event_value:
            self.extracted_query_pages += event_value.pop("extracted_query_pages")
            self._event_value_dict["extracted_query_pages"] = self.extracted_query_pages
        if "total_posts" in event_value:
            self.total_posts = event_value.pop("total_posts")
            self._event_value_dict["total_posts"] = self.total_posts
        if "pic_saved" in event_value:
            self.pic_saved += event_value.pop("pic_saved")
            self._event_value_dict["pic_saved"] = self.pic_saved
        if "tag_of_pics" in event_value:
            self.tag_of_pics.update(event_value.pop("tag_of_pics"))
            self._event_value_dict["tag_of_pics"] = self.tag_of_pics
        if "keywords" in event_value:
            self.keywords = event_value.pop("keywords")
            self._event_value_dict["keywords"] = self.keywords
        if "pic_already_exist" in event_value:
            self.pic_already_exist += event_value.pop("pic_already_exist")
            self._event_value_dict["pic_already_exist"] = self.pic_already_exist
        if "failed_urls" in event_value:
            failed_url, reason = event_value.pop("failed_urls")
            self.failed_urls[failed_url] = reason
            self._event_value_dict["failed_urls"] = self.failed_urls

    def report(self, mode="Brief"):
        if mode == "Brief":
            return "Task name: %s" % self.task_name \
                + "\nKeywords: %s" % self.keywords \
                + "\nTotal post: %s" % self.total_posts \
                + "\nSaved pictures: %s" % self.pic_saved \
                + "\nSkipped pictures: %s" % self.pic_already_exist \
                + "\nFailed requests: %s" % len(self.failed_urls)
