# the extractor that might be able to apply on all booru-like sites.
import bs4


class PicTagExtractor:
    """put a post response and get everything you want."""
    def __init__(self, pic_response):  # pic page response, not response.text
        self._soup = bs4.BeautifulSoup(pic_response.text, features='lxml')
        tag_list = self._soup.find(id='tag-list')
        self._pic_tag = dict()
        self.classify_tag(tag_list)

        self.pic_url = self._soup.find(id='post-info-size').a['href']
        # self.pic_url = self._soup.find(id='post-option-download').a['href']

    def classify_tag(self, tag_list):
        tag_types = tag_list.find_all('ul')
        # prepare types
        for t in tag_types:
            if not self._pic_tag.get(t['class'][0]):
                self._pic_tag[t['class'][0]] = dict()
            for tag in t.find_all('li'):
                self._pic_tag[t['class'][0]][tag['data-tag-name']] = int(tag.span['title'])

    def report_tags(self):
        pic_tags = dict()
        for tag_type in self._pic_tag:
            for tag, titles in self._pic_tag[tag_type].items():
                pic_tags[tag] = titles
        return pic_tags

    def show_tags(self):
        for tag_type, tag_names in self._pic_tag.items():
            print(tag_type)
            for tag in tag_names:
                print('\t%s: %s' % (tag, tag_names[tag]))

    def has_tag(self, tag: str):
        if tag in self.report_tags():
            return True
        else:
            return False

    def has_tags(self, *tags):
        counter = 0
        for tag in tags:
            if self.has_tag(tag):
                counter += 1
        return counter

    @property
    def raw_tags(self):
        return self._pic_tag

    @property
    def artist(self):
        if self._pic_tag.get('artist-tag-list'):
            return tuple(self._pic_tag['artist-tag-list'].keys())
        else:
            return "Unknown_artist"

    @property
    def character(self):
        if self._pic_tag.get('character-tag-list'):
            return tuple(self._pic_tag['character-tag-list'].keys())
        else:
            return 'unknown_character'

    @property
    def copyright(self):
        if self._pic_tag.get('copyright-tag-list'):
            return tuple(self._pic_tag['copyright-tag-list'].keys())
        else:
            return "unknown_copyright"

    @property
    def meta(self):
        if self._pic_tag.get('meta-tag-list'):
            return tuple(self._pic_tag['meta-tag-list'].keys())
        else:
            return None

    @property
    def general(self):
        if self._pic_tag.get('general-tag-list'):
            return tuple(self._pic_tag['general-tag-list'].keys())
        else:
            return None

    @property
    def tag_list(self):
        return list(self.artist) + list(self.copyright) + list(self.general) + list(self.meta)

    @property
    def md5(self):
        md5_code = self.pic_url[self.pic_url.rfind('_') + 1:self.pic_url.rfind('.')]
        return md5_code

    @property
    def format(self):
        pic_format = self.pic_url[self.pic_url.rfind('.') + 1:]
        return pic_format

    @property
    def one_line_tags(self):
        line = self.pic_url + "\t" + self.md5 + "\t"
        line += ", ".join(self.artist) + "\t"
        line += ", ".join(self.character) + "\t"
        line += ", ".join(self.copyright) + "\t"
        if self.general:
            line += "\t".join(self.general)
        return line

    @property
    def pic_name(self):
        return self.pic_url[self.pic_url.rfind('/') + 1:]


class PicInfoContent(PicTagExtractor):
    def __init__(self, pic_response, content=None):
        """
        PicTagExtractor with pic content(bytes_object) for file_manager to save things.
        :param pic_response: response_object
        """
        self.content = content
        super().__init__(pic_response)
