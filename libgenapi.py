# LibGenAPI
# by PastVision
from bs4 import BeautifulSoup
import requests

# request /search.php -> {
# req="searchTerm",
# lg_topic=[
#   libgen=non-fiction,
#   fiction=fiction,
#   scimag=science,
#   magzdb=magazines
# ],
# open=0,
# view=simple,
# res=[25,50,100] - results per page,
# phrase=1,
# column=def
# }


def error_callback(err):
    print(f"[ERROR] >> {err}\n")
    input('Press Any Key to exit...')
    quit(1)


class Book:
    def __init__(self, title, author, language, format, link) -> None:
        self.title = title
        self.author = author
        self.language = language
        self.format = format
        self.link = link


class LibGenAPI:
    HEADER = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}

    def __init__(self, error_cb) -> None:
        self.URL = None
        self.ErrorCallback = error_cb
        self.MIRRORS = ["http://libgen.is/",
                        "http://libgen.rs/",
                        "http://libgen.lt/"]
        self.SEARCH = "search.php"
        self.select_mirror()

    def select_mirror(self) -> None:
        for mirror in self.MIRRORS:
            response = requests.get(mirror)
            if response.status_code == 200:
                self.URL = mirror + self.SEARCH
                return
        if self.URL == None:
            self.ErrorCallback("LibGen Not Reachable")

    def search(
        self,
        req: str,
        lg_topic: str = 'fiction',
        open_='0',
        view='simple',
        res=25,
        phrase='1',
        column='def'
    ):
        response = requests.get(self.URL, params={
            'req': req,
            'lg_topic': lg_topic,
            'open': open_,
            'view': view,
            'res': res,
            'phrase': phrase,
            'column': column
        },
            headers=self.HEADER)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content.decode(), 'html5lib')
            table = soup.find('table', {'class': 'catalog'})
            paginator = soup.find('div', {'class': 'catalog_paginator'})
            if paginator == None:
                self.ErrorCallback("No Results Found")
            count = int(
                paginator.find('div', {'style': 'float:left'}).getText().split(' ')[0])
            rows = table.tbody.findAll('tr')
            # print(rows[0].findAll('td'))
            if count > 0:
                for row in rows:
                    col = row.findAll('td')
                    auth = col[0].ul.li.getText()
                    title = col[2].p.a.getText().strip()
                    lang = col[3].getText().strip()
                    form, size = col[4].getText().strip().split(' / ')
                    print(
                        f"Auth: {auth}\nTitle: {title}\nLang: {lang}\nFormat: {form}\nSize: {size}")
                # Fetched Data Perfectly
                # TODO get links, merge duplicates:
                for i, row in enumerate(rows):
                    a = row.findAll('a')
                    author = a[0].getText()
                    title = a[1].getText()
                    for x, y in enumerate(a):
                        break
                        # print(x, y)

                        # print(f"\n{i+1}.\tTitle: {title}\n\tAuthor: {author}")
                        # print(a)
            else:
                self.ErrorCallback("No Results Found")


if __name__ == '__main__':
    API = LibGenAPI(error_callback)
    print(f"[DEBUG] >> Using {API.URL}")
    a = " Nicholas"
    q = "The Notebook"
    API.search(req=q+a)
    # API.search(req=input("Search query >> "))
