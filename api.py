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


class LibGenAPI:

    def __init__(self, error_cb) -> None:
        self.URL = None
        self.ErrorCallback = error_cb
        self.MIRRORS = ["http://libgen.rs/",
                        "http://libgen.is/",
                        "http://libgen.st/"]
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
        })
        if response.status_code == 200:
            soup = BeautifulSoup(response.content.decode(), 'lxml')
            table = soup.find('table', {'class': 'catalog'})
            paginator = soup.find('div', {'class': 'catalog_paginator'})
            pages = int(
                soup.find('div', {'style': 'float:left'}).getText().split(' ')[0])
            rows = table.tbody.findAll('tr')
            print(pages)


if __name__ == '__main__':
    API = LibGenAPI(error_callback)
    print(f"[DEBUG] >> Using {API.URL}")
    API.search(req="notebook")
