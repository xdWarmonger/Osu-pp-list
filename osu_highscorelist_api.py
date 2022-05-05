#!/usr/bin/env python
# -*- encoding: utf-8

from tkinter import filedialog
from tkinter import Tk
import requests
import json
from types import SimpleNamespace
import os
from dotenv import load_dotenv
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.popup import Popup
from kivy.properties import StringProperty
from kivy.config import Config
# import pandas as pd
# import tabloo

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


class Osuapi:
    def __init__(self):
        # Get Client-Credentials access token from osu api
        load_dotenv()
        client_secret = os.getenv('client_secret')
        p_data = {'client_id': '4675', 'client_secret': client_secret,
                  'grant_type': 'client_credentials', 'scope': 'public'}
        p = requests.post('https://osu.ppy.sh/oauth/token/', json=p_data)
        self.client_credentials = json.loads(p.text, object_hook=lambda d: SimpleNamespace(**d))

    def api_request(self, request_link):
        r_headers = {'Content_Type': 'application/x-www-form-urlencoded',
                     'Authorization': 'Bearer ' + self.client_credentials.access_token}
        r = requests.get('https://osu.ppy.sh/api/v2' + request_link, headers=r_headers, params={'scope': 'public'})
        tmp = None
        if r.status_code == 200:
            tmp = r.json()
        return tmp


class RecycleViewRow(BoxLayout):
    name = StringProperty('')
    rank = StringProperty('')
    pp = StringProperty('')
    acc = StringProperty('')
    country_code = StringProperty('')


class Window(BoxLayout):
    def build(self):
        self.add_widget(Menu())
        self.add_widget(TbContent())
        self.add_widget(BottomMenu())
        return self.root

    @staticmethod
    def save():
        file = filedialog.asksaveasfile(mode="w", defaultextension=".txt", filetypes=[('Textfile', '.txt')])
        if file:
            for x in App.get_running_app().usercache:
                file.write("/users/" + str(x.id) + "/\n")

    @staticmethod
    def load():
        # noinspection PyBroadException
        try:
            file = filedialog.askopenfile(mode="r", filetypes=[('Textfile', '.txt')])
            id_list = []
            for line in file:
                id_list.append(line.rstrip())
            App.get_running_app().usercache = []
            App.get_running_app().load_from_file(id_list)
        except Exception:
            pass

    @staticmethod
    def startup():
        with open('D:/Users/Vincent/Documents/test1.txt') as file:
            id_list = []
            for line in file:
                id_list.append(line.rstrip())
            App.get_running_app().usercache = []
            App.get_running_app().load_from_file(id_list)

    @staticmethod
    def add_player():
        PlayerPopup().open()

    def refresh(self):
        self.ids['table_content'].refresh()


class Menu(BoxLayout):
    pass


class BottomMenu(BoxLayout):
    pass


class TbContent(RecycleView):

    def refresh(self):
        usercache = App.get_running_app().usercache

        '''df = pd.json_normalize(usercache)
        print(usercache[0])
        test_keys = ('username', 'statistics.global_rank', 'statistics.pp', 'statistics.hit_accuracy', 'country.code')
        tmp = []
        for i in range(len(usercache)):
            tmp_dict = {}
            for key in test_keys:
                item = df.at[i, key]
                tmp_dict[key] = item
            tmp.append(tmp_dict)
        self.data = tmp
        # print(tmp)'''

        rows = len(usercache)
        self.data = [{'name': str(usercache[x]['username']),
                      'rank': str(usercache[x]['statistics']['global_rank']),
                      'pp': str(usercache[x]['statistics']['pp']),
                      'acc': str(usercache[x]['statistics']['hit_accuracy']),
                      'country_code': str(usercache[x]['country']['code'])
                      } for x in range(rows)]


class PlayerPopup(Popup):
    error = StringProperty()

    def on_error(self, lbl, error_text):
        if error_text:
            self.lb_error.size_hint_y = 1
            self.size = (400, 150)
        else:
            self.lb_error.size_hint_y = None
            self.lb_error.height = 0
            self.size = (400, 120)

    def _enter(self):
        text = self.ids['input'].text
        if not text:
            self.error = "Error: Enter a username before pressing 'Enter'"
        else:
            status = App.get_running_app().add_user(text)
            if status == 0:
                self.error = f"User '{text}' successfully added"
                self.ids['input'].text = ""
            elif status == 1:
                self.error = f"User '{text}' not found"
            elif status == 2:
                self.error = f"User '{text}' already in list"

    def _cancel(self):
        self.dismiss()


class ListGuiApp(App):
    title = "Vivago's Highscorelist"
    o = Osuapi()
    usercache = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.window = None

    def load_from_file(self, id_list):
        for i in id_list:
            tmp = self.o.api_request(i)
            if tmp is not None:
                self.usercache.append(tmp)
        self.window.refresh()

    def build(self):
        self.window = Window()
        Window().startup()
        return self.window

    def add_user(self, name):
        """returns an int: \n
        0 if api request was successful \n
        1 if api request returns an error \n
        2 if user already exists in table"""
        success = 1
        if any(x['username'].lower() == name.lower() for x in self.usercache):
            success = 2
        if success != 2:
            tmp = App.get_running_app().o.api_request(f'/users/{name}/')
            if tmp is not None:
                self.usercache.append(tmp)
                success = 0
            self.window.refresh()
        return success


def main():
    Tk().withdraw()
    ListGuiApp().run()


if __name__ == '__main__':
    main()
