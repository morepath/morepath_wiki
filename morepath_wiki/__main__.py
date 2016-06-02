import morepath
from .app import App


def default_storage_directory():
    """Use a directory 'contents' in the current working directory."""
    import os
    path = './contents'
    try:
        os.mkdir(path)
    except OSError:
        if not os.path.isdir(path):
            raise
    return os.path.abspath(path)


def run():   # pragma: no cover
    App.setting('storage', 'path')(default_storage_directory)
    morepath.autoscan()
    morepath.run(App())


if __name__ == '__main__':   # pragma: no cover
    run()
