import requests
from bs4 import BeautifulSoup


class Scraping:
    def __init__(self):
        self.page = 1

        self.start = 0
        self.length = 20
        self.keyword = ''

    def new_cookie(self, type='a'):
        get_url = requests.get('[REDACTED]')
        new = get_url.cookies.values()

        if len(new) != 0:
            with open('cookies.txt', type) as cookie_file:
                print(new[0], file=cookie_file)

        return new[0]

    def get_cookie(self):
        cookie = ''

        try:
            with open('cookies.txt', 'r') as cookie_file:
                lines = cookie_file.readlines()
                cookie = self.new_cookie() if len(lines) == 0 else \
                    lines[-1].strip()
        except FileNotFoundError:
            self.new_cookie('w')

        return cookie

    def get_response(self):
        cookies = {'PHPSESSID': self.get_cookie()}

        START, LENGTH, KEYWORD = [str(i) for i in (
            self.start, self.length + 1, self.keyword)]

        data = {
            'draw': '1',
            'columns[0][data]': '0',
            'columns[0][name]': '',
            'columns[0][searchable]': 'true',
            'columns[0][orderable]': 'true',
            'columns[0][search][value]': '',
            'columns[0][search][regex]': 'false',
            'columns[1][data]': '1',
            'columns[1][name]': '',
            'columns[1][searchable]': 'true',
            'columns[1][orderable]': 'false',
            'columns[1][search][value]': '',
            'columns[1][search][regex]': 'false',
            'columns[2][data]': '2',
            'columns[2][name]': '',
            'columns[2][searchable]': 'true',
            'columns[2][orderable]': 'false',
            'columns[2][search][value]': '',
            'columns[2][search][regex]': 'false',
            'columns[3][data]': '3',
            'columns[3][name]': '',
            'columns[3][searchable]': 'true',
            'columns[3][orderable]': 'false',
            'columns[3][search][value]': '',
            'columns[3][search][regex]': 'false',
            'columns[4][data]': '4',
            'columns[4][name]': '',
            'columns[4][searchable]': 'true',
            'columns[4][orderable]': 'true',
            'columns[4][search][value]': '',
            'columns[4][search][regex]': 'false',
            'order[0][column]': '0',
            'order[0][dir]': 'asc',
            'start': START,
            'length': LENGTH,
            'search[value]': KEYWORD,
            'search[regex]': 'false'
        }

        return requests.post(
            '[REDACTED]',
            cookies=cookies,
            data=data,
            verify=False
        )


def tag_text(string):
    return BeautifulSoup(string, 'html.parser').get_text()
