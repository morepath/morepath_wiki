# reusable storage implementation for wiki taken from here
# https://bitbucket.org/r1chardj0n3s/web-micro-battle/
import cgi
import os
import re
import stat
import time

from . import html

wikiname_re = re.compile('((?<![a-z\d])([A-Z][a-z]+([A-Z][a-z]+|\d+)+))')


def wikify(text):
    return wikiname_re.sub(r'<a href="/\1">\1</a>', cgi.escape(text))


class Storage(object):
    def __init__(self, directory):
        self.directory = directory

    def get_current(self, title, create=False):
        current_file = os.path.join(self.directory, title, 'current')
        if os.path.exists(current_file):
            with open(current_file) as f:
                version_file = f.read()
            version = os.path.basename(version_file)
            version = version.split('-')[1]
        elif not create:
            raise KeyError(title)
        else:
            os.mkdir(os.path.join(self.directory, title))
            # os.path.join(self.directory, title, 'version-1')
            version_file = ''
            version = '0'

        return current_file, version_file, version

    def update_current(self, title, version_file):
        current_file = os.path.join(self.directory, title, 'current')
        if os.path.exists(current_file):
            os.remove(current_file)

        # move the current version
        with open(current_file, 'w') as f:
            f.write(version_file)

    def store_page(self, title, content):
        current, version_file, version = self.get_current(title,
                                                          create=True)

        # new version
        new_version = int(version) + 1
        version_file = os.path.join(self.directory, title,
                                    'version-%d' % new_version)

        with open(version_file, 'w') as f:
            f.write(content)

        self.update_current(title, version_file)
        return new_version

    def retrieve_page(self, title, version=None):
        dir = os.path.join(self.directory, title)
        if not os.path.exists(dir):
            raise KeyError(title)

        if version is None:
            current_file, version_file, version = self.get_current(title)
        else:
            version_file = os.path.join(dir, 'version-%s' % version)
            if not os.path.exists(version_file):
                raise KeyError(version_file)

        with open(version_file) as f:
            content = f.read()
        return content

    def revert_page(self, title, version):
        current_file = os.path.join(self.directory, title, 'current')
        if not os.path.exists(current_file):
            raise KeyError(title)

        version = os.path.join(self.directory, title, 'version-%s' % version)
        with open(current_file, 'w') as f:
            f.write(version)

    def list_page_versions(self, title):
        dir = os.path.join(self.directory, title)
        if not os.path.exists(dir):
            raise KeyError(title)

        # determine the current version
        current_file, version_file, version = self.get_current(title,
                                                               create=True)

        versions = []
        for i in range(int(version)):
            path = os.path.join(dir, 'version-%d' % (i + 1))
            mtime = os.stat(path)[stat.ST_MTIME]
            versions.append((mtime, str(i + 1)))
        versions.sort()
        return [(v, t) for t, v in versions]

    def render_page(self, name):
        try:
            content = self.retrieve_page(name)
        except KeyError:
            content = 'Page does not exist: edit to create it.'
        h = html.HTML()
        h.h1(name, id='title')
        h.pre(wikify(content), escape=False, id='content')
        h.a('edit this page', href='/%s/edit' % name, id='edit-link')
        h.br
        h.a('page history', href='/%s/history' % name, id='history-link')
        return str(h)

    def render_edit_form(self, name):
        try:
            content = self.retrieve_page(name)
        except KeyError:
            content = 'Page does not exist: edit to create it.'
        h = html.HTML()
        h.h1('Editing ' + name, id='title')
        f = h.form(action='/%s/edit' % name, method='POST')
        f.textarea(content, rows='10', cols='60', name='content')
        f.br
        f.input(type='submit', name='submit', value='Save Changes')
        f.input(type='submit', name='cancel', value='Cancel')
        return str(h)

    def render_history_form(self, name):
        h = html.HTML()
        h.h1('History For ' + name, id='title')
        h.p('Select version to revert to.')
        f = h.form(action='/%s/history' % name, method='POST')
        for version, ts in self.list_page_versions(name):
            l = f.li(time.asctime(time.localtime(ts)))
            l.input(type='radio', value=str(version), name='version')
        f.br
        f.input(type='submit', name='submit', value='Revert To Selected')
        f.input(type='submit', name='cancel', value='Cancel')
        return str(h)
