from requests_html import HTMLSession
from bs4 import BeautifulSoup

SESSION = HTMLSession()
URL = '[REDACTED]'
URL_INFO = '[REDACTED]'
URL_SCHED = '[REDACTED]' # + sched code
    

PAGE = 1
START = '0'         # int(LENGTH) * (PAGE - 1)
LENGTH = '20'       # Can be 20, 25, 50, -1; CAN BE ANY NUMBER???????
KEYWORD = ''        # Search keywords
SCHED_CODE = ''


TABLE_HEADERS = []  # [REDACTED]

def new_cookie(Type='a'):
    get_url = SESSION.get(URL)
    new = get_url.cookies.values()

    if len(new) != 0:
        with open('cookies.txt', Type) as cookie_file:
            print(new[0], file=cookie_file)

    return new[0]

def get_cookie():
    cookie = ''

    try:    
        with open('cookies.txt', 'r') as cookie_file:
            lines = cookie_file.readlines()
            cookie = new_cookie() if len(lines) == 0 else lines[-1].strip()
    except FileNotFoundError:
        new_cookie('w')
        
    return cookie

cookies = {
    'PHPSESSID': get_cookie()
}

headers = {
    # [REDACTED]
}

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

def get_response(L, K, S):
    L, K, S = [str(i) for i in (L, K, S)]
        
    D = data
    D['length'] = L
    D['search[value]'] = K
    D['start'] = S

    response = SESSION.post(URL_INFO,
##                            headers=headers,
                            cookies=cookies,
                            data=D,
                            verify=False)
    return response

def tag_parse_text(string):
    return BeautifulSoup(string, 'html.parser').get_text()

show_menu = True
while show_menu:
    Online = True
    if Online: 
        response = get_response(LENGTH, KEYWORD, START)
        json_dict = response.json()
    else:
        response_json = {}  # [REDACTED]
        json_dict = response_json
    
    json_data = json_dict['data']

    print('{:<15.15} {:<23.20} {:<15.15} {:<10.10} {:<15.15}'.format(*TABLE_HEADERS))
    for data_row in json_data:
        data_row = [tag_parse_text(d) for d in data_row]

        print('{:<15.15} {:<23.20} {:<15.15} {:<10.10} {:<15.15}'.format(*data_row))

    print('', 'MENU LOLOLOLOL [If no data, try to refresh cookies]',
          f'Number of rows to display: {LENGTH}',
          f'Searching for the keywords: {KEYWORD}',
          '[1] Next page',
          '[2] Previous page',
          '[3] Change number of displayed rows',
          '[4] Search for a keyword',
          '[5] Search for a schedule code',
          '[6] Refresh cookies',
          '[0] End program', sep='\n')

    selection = input('Please make a selection: '); print()
    if selection.isdigit(): selection = int(selection)

    if selection == 1:
        PAGE += 1
        START = int(START) + int(LENGTH)

    elif selection == 2:
        if PAGE == 1:
            print('This is the start of the entries!')
        else:
            PAGE -= 1
            START = int(START) - int(LENGTH)

    elif selection == 3:
        user = input('Enter number of rows desired: ')
        if user.isdigit(): LENGTH = int(user)

    elif selection == 4:
        KEYWORD = input('Enter keyword(s) to search for: ')
        PAGE = 1
        START = 0

    elif selection == 5:
##        print('To implement!')
        
        SCHEDULE_CODE = input('Enter schedule code: ')

        RESPONSE = SESSION.get(URL_SCHED + SCHEDULE_CODE)
        SOUP = BeautifulSoup(RESPONSE.html.html, 'html.parser')

        valid_code = True
        class_info = SOUP.find_all('div', {'class':'profile-info-row'})
        information = [info.get_text().strip().split('\n') for info in class_info]
        for i in information:
            if i[0] == 'Section' and len(i) == 1:
                valid_code = False

        if not valid_code:
            print('There was a problem in getting information from given schedule code.')
        else:
            print('CLASS INFORMATION')
            class_info = SOUP.find_all('div', {'class':'profile-info-row'})
            for info in class_info:
                info_text = info.get_text().strip().split('\n')

                if info_text[0] == 'Note ': continue

                print('{:<20} {}'.format(*info_text))
            print()

            print('STUDENT LIST')
            row_list = SOUP.find_all('tr')
            for row in row_list:
                row_data = row.get_text().strip().split('\n')

                print('{:<3.3} {:<30.30} {:<16.16} {:<8.8} {:<8.8} {:<10.10}'.format(*row_data))

    elif selection == 6:
        print('Trying to fetch new cookies. . .')
        new_cookie()

    elif selection == 0:
        print('Thank you very much!')
        show_menu = False

    else:
        print('You have made an invalid selection!')


    if selection not in (0, 1, 2): input('\nPress Enter to continue. . .'); print()

      





