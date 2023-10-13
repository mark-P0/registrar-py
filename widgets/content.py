from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.font_definitions import theme_font_styles
import kivymd.material_resources as m_res

from kivymd.toast.kivytoast.kivytoast import toast
from kivymd.uix.behaviors import RectangularRippleBehavior
from kivymd.uix.dialog import MDInputDialog

from kivy.properties import (
    StringProperty, OptionProperty, ListProperty,
    NumericProperty, BooleanProperty
)
from kivy.clock import Clock
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout

from scripts import core


class Contents(GridLayout):
    def __init__(self, **kwargs):
        super(Contents, self).__init__(**kwargs)

        self.registrar = core.Scraping()
        self.data = None
        self.searching = False

        try:
            self.registrar.new_cookie()
            self.retrieve_subjects()
        except Exception as e:
            print('Error in starting application:', e)

            toast('Cannot establish connection.')

    def open_prompt(self):
        MDInputDialog(
            title='Enter keywords:',
            hint_text='hmm',
            text_button_ok='Search',
            size_hint=(0.8, 0.4),
            events_callback=self.search_keywords
        ).open()

    def search_keywords(self, button_text, instance):
        self.searching = True

        self.registrar.keyword = instance.text_field.text
        current_app = MDApp.get_running_app()
        current_app.root.current_keyword = f'"{self.registrar.keyword}"'
        current_app.root.ids.app_toolbar.title = f'"{self.registrar.keyword}"'
        current_app.root.ids.app_toolbar.right_action_items = [
            ['close', self.close_search],
            ["chevron-left", self.previous_page],
            ["chevron-right", self.next_page]
        ]

        self.registrar.page = 1
        self.registrar.start = 0

        self.retrieve_subjects()

    def close_search(self, *args):
        self.searching = False

        self.registrar.keyword = ''
        current_app = MDApp.get_running_app()
        current_app.root.current_keyword = ''
        current_app.root.ids.app_toolbar.title = 'Enrollment Information'
        MDApp.get_running_app().root.ids.app_toolbar.right_action_items = [
            ["chevron-left", self.previous_page],
            ['numeric-1', lambda x: x],
            ["chevron-right", self.next_page]
        ]

        self.registrar.page = 1
        self.registrar.start = 0

        self.retrieve_subjects()

    def refresh_cookies(self):
        try:
            old = self.registrar.get_cookie()
            new = self.registrar.new_cookie()
            print(
                f'Old cookie: {old}',
                f'New cookie: {new}',
                sep='\n'
            )

            self.registrar.page = 1
            self.registrar.start = 0

            MDApp.get_running_app().root.ids.app_toolbar.right_action_items = [
                ["chevron-left", self.previous_page],
                ['numeric-1', lambda x: x],
                ["chevron-right", self.next_page]
            ]

            if self.searching:
                self.close_search()
            else:
                self.retrieve_subjects()
        except Exception as e:
            print('Error in refreshing cookies:', e)

            toast('Error in getting new cookies.')

    def next_page(self, *args):
        if self.actual_length <= self.registrar.length:
            toast('There are no more records under this criteria.')
        else:
            self.registrar.page += 1
            self.registrar.start += self.registrar.length

            current_page = self.registrar.page
            digit = 10 if current_page == 10 else current_page % 10

            MDApp.get_running_app().root.ids.app_toolbar.right_action_items = [
                ["chevron-left", self.previous_page],
                [f'numeric-{digit}', lambda x: x],
                ["chevron-right", self.next_page]
            ] if not self.searching else [
                ['close', self.close_search],
                ["chevron-left", self.previous_page],
                ["chevron-right", self.next_page]
            ]

            self.retrieve_subjects()

    def previous_page(self, *args):
        if self.registrar.page == 1:
            toast('This is the first page.')
        else:
            self.registrar.page -= 1
            self.registrar.start -= self.registrar.length

            current_page = self.registrar.page
            digit = 10 if current_page == 10 else current_page % 10

            MDApp.get_running_app().root.ids.app_toolbar.right_action_items = [
                ["chevron-left", self.previous_page],
                [f'numeric-{digit}', lambda x: x],
                ["chevron-right", self.next_page]
            ] if not self.searching else [
                ['close', self.close_search],
                ["chevron-left", self.previous_page],
                ["chevron-right", self.next_page]
            ]

            self.retrieve_subjects()

    def retrieve_subjects(self):
        self.clear_widgets()

        try:
            response = self.registrar.get_response()
            json = response.json()
            self.actual_length = len(json['data'])
            self.data = json['data'][:self.registrar.length]

            self.current_index = 0
            self.deferred_adding = Clock.schedule_interval(self.add_card, 0.1)
        except Exception as e:
            print('Error in getting subjects:', e)

            toast('Cannot establish connection.')

    def add_card(self, *args):
        if self.current_index == len(self.data):
            self.deferred_adding.cancel()
            return

        item = [core.tag_text(element) for element in self.data[self.current_index]]

        max_length = 30

        full_name = item[1]
        split = [item for item in item[1].split(' ') if item != '']

        first_line = ''
        index = 1
        while True:
            consider = split[:(index * -1)]

            if len(consider) == 1 or len(split) == 1:
                if len(split) == 1:
                    consider = [split[0]]

                if len(consider[0]) > (max_length // 2):
                    first_line = consider[0][:(max_length // 2) - 3] + '...'
                else:
                    first_line = consider[0]

                for word in consider:
                    split.remove(word)

                break

            combined = ' '.join(consider)

            if len(combined) <= (max_length // 2) + 3:
                first_line = combined

                for word in consider:
                    split.remove(word)

                break

            index += 1

        temp = ' '.join(split)
        second_line = temp[:(max_length // 2) - 3] + '...' \
            if len(temp) > (max_length // 2) else temp

        name = '{} {}'.format(
            first_line, '' if second_line == '' else second_line)

        # subject_code = item[0]
        schedule_code = item[2]
        section = item[3]
        slots = item[4]

        new_card = ContentCardListItem(
            subject_code=str(schedule_code),
            subject_name=str(name),
            subject_name_full=str(full_name),
            section=str(section),
            slots=str(slots)
        )

        self.add_widget(new_card)
        self.current_index += 1


class ContentCardListItem(
    ThemableBehavior, RectangularRippleBehavior, ButtonBehavior, FloatLayout
):
    divider = None

    subject_code = StringProperty()
    subject_name = StringProperty()
    subject_name_full = StringProperty()
    section = StringProperty()
    slots = StringProperty()

    text = StringProperty()
    text_color = ListProperty(None)
    font_style = OptionProperty("Subtitle1", options=theme_font_styles)
    theme_text_color = StringProperty("Primary", allownone=True)
    secondary_text = StringProperty()
    tertiary_text = StringProperty()
    secondary_text_color = ListProperty(None)
    tertiary_text_color = ListProperty(None)
    secondary_theme_text_color = StringProperty("Secondary", allownone=True)
    tertiary_theme_text_color = StringProperty("Secondary", allownone=True)
    secondary_font_style = OptionProperty("Body1", options=theme_font_styles)
    tertiary_font_style = OptionProperty("Body1", options=theme_font_styles)
    divider = OptionProperty(
        "Full", options=["Full", "Inset", None], allownone=True
    )
    bg_color = ListProperty()
    _txt_left_pad = NumericProperty("16dp")
    _txt_top_pad = NumericProperty()
    _txt_bot_pad = NumericProperty()
    _txt_right_pad = NumericProperty(m_res.HORIZ_MARGINS)
    _num_lines = 3
    _no_ripple_effect = BooleanProperty(False)
