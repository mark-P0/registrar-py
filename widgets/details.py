from kivymd.uix.list import TwoLineIconListItem
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout

import requests
from bs4 import BeautifulSoup


class DetailSection(BoxLayout):
    code = StringProperty('N/A')
    generalinfo = ObjectProperty(None)
    detaillist = ObjectProperty(None)

    def pass_control(self, current_code):
        self.code = current_code
        self.retrieve_information()

    def retrieve_information(self):
        url_specific = '[REDACTED]'

        response = requests.get(url_specific + self.code)
        soup = BeautifulSoup(response.text, 'html.parser')

        self.detaillist.clear_widgets()

        valid_code = True
        class_info = soup.find_all('div', {'class': 'profile-info-row'})
        information = [
            info.get_text().strip().split('\n') for info in class_info]

        for i in information:
            if i[0] == 'Section' and len(i) == 1:
                valid_code = False

        if not valid_code:
            self.generalinfo.text = 'There was a problem in getting information from given schedule code.'
            print(self.generalinfo.text)
            return

        general_info_string = ''
        general_info_string += 'CLASS INFORMATION\n'
        for info in class_info:
            info_text = info.get_text().strip().split('\n')

            if info_text[0] == 'Note ':
                continue

            general_info_string += '{:<20} {}\n'.format(*info_text)

        general_info_string += '\n'
        self.generalinfo.text = general_info_string

        row_list = soup.find_all('tr')

        for row in row_list[1:]:
            row_data = row.get_text().strip().split('\n')

            name = row_data[1].split(', ')

            self.detaillist.add_widget(
                DetailListItem(
                    line_1=' '.join(
                        [n.lower().capitalize() for n in name[0].split(' ')]
                    ),
                    line_2=f'{name[1]} • {row_data[3]} • {row_data[2]}',
                    gender=row_data[4].lower(),
                )
            )


class DetailListItem(TwoLineIconListItem):
    line_1 = StringProperty()
    line_2 = StringProperty()
    gender = StringProperty()
    action = StringProperty()

    divider = None
