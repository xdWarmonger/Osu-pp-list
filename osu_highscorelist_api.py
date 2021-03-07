import requests
import json
from types import SimpleNamespace
import os
from dotenv import load_dotenv
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.properties import StringProperty
from kivy.config import Config


# Config.set('graphics', 'resizable', False)
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


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

    def save(self):
        print('saving...')

    def load(self):
        print('loading...')

    def add_player(self):
        PlayerPopup().open()


class Menu(BoxLayout):
    pass


class BottomMenu(BoxLayout):
    pass


class TbContent(RecycleView):
    def __init__(self, **kwargs):
        super(TbContent, self).__init__(**kwargs)
        rows = len(usercache)
        self.data = [{'name': str(usercache[x].username),
                      'rank': str(usercache[x].statistics.pp_rank),
                      'pp': str(usercache[x].statistics.pp),
                      'acc': str(usercache[x].statistics.hit_accuracy),
                      'country_code': str(usercache[x].country.code)
                      } for x in range(rows)]

    def refresh(self):
        rows = len(usercache)
        self.data = [{'name': str(usercache[x].username),
                      'rank': str(usercache[x].statistics.pp_rank),
                      'pp': str(usercache[x].statistics.pp),
                      'acc': str(usercache[x].statistics.hit_accuracy),
                      'country_code': str(usercache[x].country.code)
                      } for x in range(rows)]


class PlayerPopup(Popup):
    error = StringProperty()

    def on_error(self, lbl, text):
        if text:
            self.lb_error.size_hint_y = 1
            self.size = (400, 150)
        else:
            self.lb_error.size_hint_y = None
            self.lb_error.height = 0
            self.size = (400, 120)

    def _enter(self):
        if not self.text:
            self.error = "Error: enter username"
        else:
            Osuapi().api_request('/users/' + str(self.text) + '/')
            TbContent().refresh()
            self.dismiss()

    def _cancel(self):
        self.dismiss()


class ListGuiApp(App):
    title = "Vivago's Highscorelist"

    def build(self):
        return Window()


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
        user_json = json.loads(r.text, object_hook=lambda d: SimpleNamespace(**d))
        usercache.append(user_json)


def main():
    for i in players_to_add:
        o.api_request(i)
    ListGuiApp().run()


if __name__ == '__main__':
    o = Osuapi()
    usercache = []
    players_to_add = ['/users/Whitecat/', '/users/Umbre/', '/users/xXVivagoXx/']
    main()
