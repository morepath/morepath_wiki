import morepath
from . import storage


class App(morepath.App):

    @morepath.reify
    def wiki(self):
        return storage.Storage(self.settings.storage.path)
