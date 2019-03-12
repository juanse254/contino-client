from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from gitHandler import gitHandler
from pollingService import pollGit

import os

result = None

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class Root(FloatLayout):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)

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

def startHandler():
    global result
    repo = gitHandler.fetchData(result)
    pollGit(repo)  # TODO:esto debe ser un hilo para que no bloquee el resto del programa.


class clientStartUp(App):
    pass


Factory.register('Root', cls=Root)
Factory.register('LoadDialog', cls=LoadDialog)


if __name__ == '__main__':
    clientStartUp().run()