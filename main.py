from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog

from kivy.utils import platform
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen

from widgets.drawer import (        # noqa: F401 [Unused because they are used by the .kv!]
    DrawerContents, DrawerContentsList, DrawerContentsListItem)
from widgets.content import (       # noqa: F401 [Unused because they are used by the .kv!]
    Contents, ContentCardListItem)
from widgets.details import (       # noqa: F401 [Unused because they are used by the .kv!]
    DetailSection, DetailListItem)


class Container(Screen):
    current_keyword = StringProperty('Enrollment Information')


class DebugDialog(MDDialog):
    def __init__(self, text, title_type, **kwargs):
        title_dict = {'good': 'Nice!',
                      'warning': 'Attention!',
                      'bad': 'Uh-oh, something happened!'}

        self.title = title_dict[title_type]
        self.text = text

        super(DebugDialog, self).__init__(**kwargs)


class Registrar(MDApp):
    def __init__(self, **kwargs):
        super(Registrar, self).__init__(**kwargs)

        self.title = 'Registrar'
        # self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Green'
        ''' Possible palettes
            'Red', 'Pink', 'Purple', 'DeepPurple', 'Indigo', 'Blue',
            'LightBlue', 'Cyan', 'Teal', 'Green', 'LightGreen', 'Lime',
            'Yellow', 'Amber', 'Orange', 'DeepOrange', 'Brown', 'Gray',
            'BlueGray' '''

    def build(self):
        return Container()

    # def on_start(self):
    #     self.fps_monitor_start()


if __name__ == '__main__':
    application = Registrar()

    if platform != 'android':
        Window.size = (360, 720)

    application.run()
