import os
import json
from common.utill import create_logger

Logger = create_logger("Chrome")


class IChrome:
    def __init__(self, bookmarks_path=None):
        self.__url_list = list()
        self.__bookmarks_json = None
        if not bookmarks_path:
            env_home_path = os.getenv("HOME")
            bookmarks_path = "{}/.config/chromium/Default/Bookmarks".format(env_home_path)
        self.bookmarks = bookmarks_path

    @property
    def bookmarks(self):
        return self.__bookmarks_json

    @bookmarks.setter
    def bookmarks(self, bookmarks_path):
        with open(bookmarks_path) as json_data:
            data = json.load(json_data)
            self.__bookmarks_json = data.get('roots').get('bookmark_bar').get('children')

    def get_folder(self, folder_name):
        for bookmark in self.bookmarks:
            if bookmark.get('type') == 'folder' and bookmark.get('name') == folder_name:
                return bookmark.get('children')
        else:
            return []

    def get_yt_urls(self, folder_name):
        url_list = []
        for kid in self.get_folder(folder_name):
            url = kid.get("url", "")
            if 'youtube' in url:
                url_list.append(url)
        Logger.info("I found {} urls".format(len(url_list)))
        return url_list


if __name__ == '__main__':
    x = IChrome()
    # print(x.bookmarks)
    print(x.get_folder("M"))
    print(x.get_yt_urls("M"))
