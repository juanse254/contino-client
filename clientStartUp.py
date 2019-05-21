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

HOST = 'http://fa2572e4.ngrok.io/'

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
        #result = gitHandler.searchGit(filename[0])
        result = gitHandler.searchGit('/Users/nicolasgordillo/Documents/uzh/fs19/masterProject/git_projects/test/Coffee')
        if result:
            startHandler()
            self.dismiss_popup()

    def show_image(self):
        global result
        #repo = gitHandler.fetchData(result) #TODO:check if we selected a repo already.
        req = post(HOST + 'getGraph/', data={'gitUrl' : 'lol'} ) #pass the repo url instead of lol
        image_url = json.loads(req.text)['graphUrl']
        webbrowser.open_new(image_url)
        if(self.svg):
            self.remove_widget(self.svg)
        #urllib.request.urlretrieve(image_url, "tmp.svg")
        self.svg = SvgWidget('tmp.svg', size_hint=(None, None))
        self.add_widget(self.svg)
        self.svg.scale = 0.5
        self.svg.center = Window.center
        #os.remove('tmp.svg')

def startHandler():
    global result
    repo = gitHandler.fetchData(result)
    pollGit(repo)  # TODO:esto debe ser un hilo para que no bloquee el resto del programa.


class clientStartUp(App):
    pass


Factory.register('Root', cls=Root)
Factory.register('LoadDialog', cls=LoadDialog)
Factory.register('SvgWidget', cls=SvgWidget)


if __name__ == '__main__':
    clientStartUp().run()