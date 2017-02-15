# !/usr/bin/env python
from __future__ import print_function

import re
import sys
from urllib.request import urlopen

import requests
from bs4 import BeautifulSoup


class TaiwanEBook:
    """
    Download E-book resource from The National Central Library (NCL) of Taiwan: http://taiwanebook.ncl.edu.tw/
    Legal download address looks like: http://taiwanebook.ncl.edu.tw/zh-tw/book/NCL-004752675
    """
    header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
        "Accept": "text/html,application/xhtml+xml,application/xml; q=0.9,image/webp,*/*;q=0.8"}

    def __init__(self, url):
        self.url = url

    def __get_download_url(self):
        url_parts = self.url.split('/')
        filename = url_parts[5] + '.PDF'
        pdf_url = url_parts[0] + '//' + url_parts[2] + '/ebkFiles/' + url_parts[5] + '/' + filename
        return pdf_url

    def __get_pdf_title(self):
        content = requests.get(url, self.header)
        soup = BeautifulSoup(content.text, 'lxml')
        title_raw = soup.findAll("h2")[1].text.split('\r\n')[1]
        title = re.sub('\W+', '', title_raw)
        return title

    def download(self):
        download_url = self.__get_download_url()
        title = self.__get_pdf_title()
        print("Downloading book: ", title)
        response = urlopen(download_url)
        file = open(title + ".pdf", 'wb')
        file.write(response.read())
        file.close()
        print("Downloading Completed")


if __name__ == "__main__":
    url = sys.argv[1]
    # url = 'http://taiwanebook.ncl.edu.tw/zh-tw/book/NCL-004752675'
    download_task = TaiwanEBook(url)
    download_task.download()