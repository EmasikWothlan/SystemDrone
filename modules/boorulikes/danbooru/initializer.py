# danbooru initializer
from modules.defaults import initializer
import os


class Initializer(initializer.Initializer):
    # TODO: is there a way to prevent from repeating download for existed picture? is database necessary to make it?
    def init(self, journal, reporter):
        keywords_string = '+'.join(journal.main_keywords)
        first_query_page = 'https://danbooru.donmai.us/posts?tags=' + keywords_string
        journal.new_urls(first_query_page)

        task_name = 'DanbooruScrape: %s' % keywords_string

        journal.console.write("Starting task: %s" % task_name)

        reporter.post(task_name=task_name, method='update')
        keywords = journal.main_keywords + journal.other_keywords

        reporter.post(keywords=keywords, method='update')

        journal.url_and_pic_info = {}

        # to check save_path is valid.
        if os.path.exists(self._config.save_path):
            pass
        else:
            raise FileNotFoundError("%s not found, you have to indicate a valid directory." % self._config.save_path)
