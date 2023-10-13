from kivymd.theming import ThemableBehavior
from kivymd.uix.list import OneLineIconListItem, MDList

from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout


class DrawerContents(BoxLayout):
    pass


class DrawerContentsList(ThemableBehavior, MDList):
    def set_color_item(self, instance_item):
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break

        instance_item.text_color = self.theme_cls.primary_color


class DrawerContentsListItem(OneLineIconListItem):
    icon = StringProperty()

    divider = None
