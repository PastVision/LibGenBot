# LibGenBot
# by PastVision
from libgenapi import LibGenAPI


def error_callback(err):
    print(f"[ERROR] >> {err}\n")
    input('Press Any Key to exit...')
    quit(1)


class LibGenBot:
    def __init__(self, API: LibGenAPI, error_cb: function) -> None:
        self.API = API
        self.ErrorCallback = error_cb


if __name__ == '__main__':
    api = LibGenAPI(error_callback)
