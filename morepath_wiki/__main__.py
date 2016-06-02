import morepath
from .app import App


def run():   # pragma: no cover
    morepath.autoscan()
    morepath.run(App())


if __name__ == '__main__':
    run()
