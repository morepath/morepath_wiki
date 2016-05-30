from . import storage
from .app import App
from .model import Root, Page


@App.path(model=Root, path='/')
def get_root():
    return Root()


@App.path(model=Page, path='{name}')
def get_page(name):
    if not storage.wikiname_re.match(name):
        return None
    return Page(name)
