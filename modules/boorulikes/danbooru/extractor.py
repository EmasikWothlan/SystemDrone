import bs4
import re

from modules.boorulikes.pic_tag_extractor import PicInfoContent, PicTagExtractor


class Extractor:
    def __init__(self, config):
        self.config = config
        self.first_query = True

    def extract(self, journal, reporter):
        """
        check url_responses:
         if it's a post, extract tags and pic_urls, tags go to pic_info, pic_urls to following_urls.
         if it's a pic_url, attach pic_info on it then put into content_to_save.
         if it's a query page, extract all posts urls and put into following_urls.
          if reporter have "first_query": True, post total posts and things like that.
        :param journal:
        :param reporter:
        :return:
        """
        for url, resp in journal.url_responses.items():
            # for query page
            if url.find('posts?') != -1:
                if self.first_query:
                    self._query_information(url, resp, journal, reporter)
                    self.first_query = False

                # extract all posts on this query page
                posts_on_this_page = self._extract_posts(resp)
                journal.new_urls(*posts_on_this_page)

                reporter.post(extracted_query_pages=1)

            # for post page
            elif url.find('posts') != -1:

                pic_info = PicInfoContent(resp)

                # filter by filter_expressions.
                for okw in journal.other_keywords:
                    if not pic_info.has_tag(okw):  # if any of the other keywords are not in the list, skip this post.
                        break
                else:
                    journal.new_urls(pic_info.pic_url)
                    journal.url_and_pic_info[pic_info.pic_url] = pic_info

                    pic_tag = PicTagExtractor(resp)
                    reporter.post(tags_of_pics={pic_tag.pic_name: pic_tag.raw_tags})

            # assume others are pic_url
            else:
                # find pic_info for this url and attach the content on it.
                pic_with_tags = journal.url_and_pic_info[url]
                pic_with_tags.content = resp.content
                # put things into content_to_save
                journal.content_to_save[url] = pic_with_tags
        journal.url_responses.clear()

    @staticmethod
    def _query_information(query_page, resp, journal, reporter):
        soup = bs4.BeautifulSoup(resp.text, features='lxml')
        metas = soup.find_all('meta')

        # determine total posts and post to reporter
        total_img = 0
        for meta in metas:
            try:
                meta_string = meta['content']
            except KeyError:  # should be KeyError
                continue
            if meta_string.startswith('See over'):
                total_img = int(re.findall("See over (.*?) ", meta_string)[0].replace(",", ""))

                journal.console.write("%s pics found by keywords %s" % (total_img, journal.main_keywords))
                break

        reporter.post(total_posts=total_img)

        # find the max page number
        max_page = 1
        page = soup.find(class_='paginator')
        numbered_pages = page.find_all(class_='numbered-page')
        if numbered_pages:
            for p in numbered_pages:
                if int(p.a.string) > max_page:
                    max_page = int(p.a.string)
            # add all page number into following_urls
            if max_page > 1:
                for i in range(2, max_page + 1):
                    journal.following_urls.append(query_page + '&' + 'page=' + str(i))
        else:
            # there's only 1 page for the query.
            pass
        reporter.post(max_query_pages=max_page)

    @staticmethod
    def _extract_posts(resp):
        soup = bs4.BeautifulSoup(resp.text, features='lxml')
        posts = soup.find(id="posts-container")
        # in case that there's just nothing.
        if posts.p and posts.p.string.find('Nobody here but us chickens!') != -1:
            # if there's some return value,
            return list()
        post_urls = []
        articles = posts.find_all('article')
        for article in articles:
            try:
                if article.a['href'].startswith('/'):
                    post_urls.append('https://danbooru.donmai.us' + article.a['href'])
                elif article.a['href'].startswith('http'):
                    post_urls.append(article.a['href'])  # I don't expect this.
            except:
                continue
        return post_urls
