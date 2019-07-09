from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from gitHandler import gitHandler
from pollingService import pollGit
from kivy.uix.scatter import Scatter
from kivy.graphics.svg import Svg
from kivy.core.window import Window
from requests import post
import urllib.request
import json
import os
import threading
import webbrowser

result = None

HOST = 'http://127.0.0.1:8000/'

class SvgWidget(Scatter):

    def __init__(self, filename, **kwargs):
        super(SvgWidget, self).__init__(**kwargs)
        with self.canvas:
            svg = Svg(filename)
            self.size = svg.width, svg.height

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class Root(FloatLayout):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)
    svg= ObjectProperty(None)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()


    def load(self, path, filename):
        global result
        result = gitHandler.searchGit(filename[0])
        if result:
            startHandler()
            self.dismiss_popup()
            self.ids.updaterButton.disabled = False
            self.ids.pickerButton.disabled = True

    def show_image(self):
        global result #TODO:disable select directory button if result exists.
        repo = gitHandler.fetchData(result) #TODO:check if we selected a repo already.
        try:
            req = post(HOST + 'getGraph/', data={'gitUrl' : repo.remotes.origin.url , 'commitUser': repo.commit().hexsha} ) #pass the repo url instead of lol
            image_url = json.loads(req.text)['graphUrl']
            webbrowser.open_new(image_url)
        except BaseException as e:
            print("Couldnt fetch data: ")
            print(e)

def startHandler():
    global result
    repo = gitHandler.fetchData(result)
    poller = threading.Thread(target=pollGit, args=(repo,), daemon=True)
    poller.start()


class clientStartUp(App):
    pass


Factory.register('Root', cls=Root)
Factory.register('LoadDialog', cls=LoadDialog)
Factory.register('SvgWidget', cls=SvgWidget)


if __name__ == '__main__':
    clientStartUp().run()