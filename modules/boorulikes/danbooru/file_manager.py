import os

from modules.defaults import file_manager


class FileManager(file_manager.FileManager):
    def save(self, journal, reporter):
        while journal.content_to_save:
            url, pic_and_content = journal.content_to_save.popitem()

            # the validation has been done in Initializer, no check needed.
            file_name = pic_and_content.pic_name

            directory_name = self.form_directory_name(journal.main_keywords, pic_and_content)
            os.makedirs(directory_name, exist_ok=True)
            abs_filename = os.path.join(self._config.save_path, directory_name, file_name)

            if os.path.exists(abs_filename):
                journal.console.write("Skip file %s\tfile already exists." % file_name)
                journal.console.write(
                    "Progress: %s/%s" % (reporter.pic_saved + reporter.pic_already_exist, reporter.total_posts))
                reporter.post(pic_already_exist=1)
            else:
                journal.console.write("Saving picture %s" % file_name)
                self._save_picture(abs_filename, pic_and_content.content)
                reporter.post(pic_saved=1)
                journal.console.write(
                    "Progress: %s/%s" % (reporter.pic_saved + reporter.pic_already_exist, reporter.total_posts))

    @staticmethod
    def _save_picture(filename, content):
        with open(filename, mode="wb") as fd:
            fd.write(content)

    def form_directory_name(self, main_keywords, description):
        """
        this will only name the directory,
        the name of the picture will keep as it is to maintain identity.

        Legendary:
        %A is artist
        %c is character
        %C is Copyright
        %M is MD5  # is there anybody want this to be a folder's name?
        %K is the main key words
        %K1 is the first main key words
        %K2 is the second key words
        / is a directory

        example:
            /- Artist - %A/%K/
            means to save the pic under save path's directory named "- Artist - ARTIST_NAME",
            and in that folder, makedir named by the main key words.
        """

        pattern = self._config.save_pattern
        # must check if any of them screw the pathname up!
        # for example: fate/stay_night
        artist = self._pathname_safe_convert("_and_".join(description.artist))
        pattern = pattern.replace("%A", artist or "UnknownArtist")
        characters = self._pathname_safe_convert("_and_".join(description.character))
        pattern = pattern.replace("%c", characters or "UnknownCharacter")
        copyright = self._pathname_safe_convert("_and_".join(description.copyright))
        pattern = pattern.replace("%C", copyright or "UnknownCopyright")
        pattern = pattern.replace("%M", description.md5)

        # these must be replaced before "%K" replacement.
        main_keywords1 = self._pathname_safe_convert(main_keywords[0])
        pattern = pattern.replace("%K1", main_keywords1)
        main_keywords2 = self._pathname_safe_convert(main_keywords[-1])
        pattern = pattern.replace("%K2", main_keywords2)
        #
        main_keywords1_2 = self._pathname_safe_convert("_".join(main_keywords))
        pattern = pattern.replace("%K", main_keywords1_2)

        directory = os.path.join(self._config.save_path, *(pattern.split("/")))
        return directory

    @staticmethod
    def _pathname_safe_convert(string: str):
        # avoiding illegal characters shown in directory name.
        string = string.replace('/', '_')
        string = string.replace('\\', '_')
        string = string.replace('|', '_')
        string = string.replace(' ', '_')
        string = string.replace('+', '_')
        string = string.replace('-', '_')
        string = string.replace('*', '_')
        string = string.replace('!', '_')
        string = string.replace('^', '_')
        string = string.replace(':', '_')
        string = string.replace(';', '_')
        return string
