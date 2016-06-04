import pytest
from webtest import TestApp as Client


@pytest.fixture(scope="module")
def App(tmpdir_factory):
    """Return the App class configured for testing.

    The wiki is stored in a temporary directory, and is shared among the tests.
    The tests are not isolated, and most depend on the state of the wiki
    reached by running the previous tests in the sequence they appear in this
    module.

    """
    from .. import App as _App, path, view   # noqa
    tmpdir = tmpdir_factory.mktemp(__name__)
    _App.setting('storage', 'path')(lambda: str(tmpdir))
    return _App


def get_text(response, css_selector):
    matches = response.html.select(css_selector)
    assert len(matches) == 1
    return matches[0].text


def test_create_frontpage(App):
    c = Client(App())

    empty_frontpage = c.get('/').follow()

    assert get_text(empty_frontpage, '#title') == \
        'FrontPage'
    assert get_text(empty_frontpage, '#content') == \
        'Page does not exist: edit to create it.'

    create_form = empty_frontpage.click(linkid='edit-link').form
    create_form['content'] = 'This is an example'
    frontpage_v1 = create_form.submit('submit').follow()

    assert get_text(frontpage_v1, '#title') == \
        'FrontPage'
    assert get_text(frontpage_v1, '#content') == \
        'This is an example'


def test_noncamelcase_page(App):
    c = Client(App())

    c.get('/foobar', status=404)


def test_abandon_page_creation(App):
    app = App()
    c = Client(app)

    empty_page = c.get('/FooBar')

    assert get_text(empty_page, '#title') == \
        'FooBar'
    assert get_text(empty_page, '#content') == \
        'Page does not exist: edit to create it.'

    create_form = empty_page.click(linkid='edit-link').form
    create_form['content'] = 'This is an example'

    # We are sent back to the front page
    response = create_form.submit('cancel').follow()
    assert get_text(response, '#title') == \
        'FrontPage'

    # We can also verify that the page is not present in the storage:
    with pytest.raises(KeyError):
        app.wiki.get_current('FooBar')

    with pytest.raises(KeyError):
        app.wiki.list_page_versions('FooBar')

    with pytest.raises(KeyError):
        app.wiki.revert_page('FooBar', '1')


def test_create_second_version(App):
    c = Client(App())

    page = c.get('/FrontPage')
    assert get_text(page, '#title') == 'FrontPage'

    create_form = page.click(linkid='edit-link').form
    create_form['content'] = 'This is a much better example'
    newversion = create_form.submit('submit').follow()

    assert get_text(newversion, '#title') == 'FrontPage'
    assert get_text(newversion, '#content') == 'This is a much better example'


def test_abandon_revert(App):
    c = Client(App())

    history = c.get('/FrontPage').click(linkid='history-link')
    assert get_text(history, '#title') == 'History For FrontPage'

    revert_form = history.form
    front = revert_form.submit('cancel').follow()

    assert get_text(front, '#title') == 'FrontPage'
    assert get_text(front, '#content') == 'This is a much better example'


def test_revert_to_first(App):
    c = Client(App())

    history = c.get('/FrontPage').click(linkid='history-link')
    assert get_text(history, '#title') == 'History For FrontPage'

    revert_form = history.form
    revert_form['version'] = '1'
    page = revert_form.submit('submit').follow()

    assert get_text(page, '#title') == 'FrontPage'
    assert get_text(page, '#content') == 'This is an example'


def test_storage(App):
    app = App()
    app.commit()

    # Version 1 exist:
    assert app.wiki.retrieve_page('FrontPage', '1') == 'This is an example'

    # Version two has been reverted but not purged:
    assert app.wiki.retrieve_page('FrontPage', '2') == \
        'This is a much better example'

    # Version three does not exist:
    with pytest.raises(KeyError):
        app.wiki.retrieve_page('FrontPage', '3')

    # You can in fact revert back to version two:
    app.wiki.revert_page('FrontPage', '2')
    assert app.wiki.retrieve_page('FrontPage') == \
        'This is a much better example'


def test_default_storage_directory(tmpdir, monkeypatch):
    from ..__main__ import default_storage_directory

    monkeypatch.chdir(tmpdir)

    contents = tmpdir.join('contents')

    assert not contents.check()
    default_storage_directory()

    assert contents.check(dir=True)

    # Verify that it is idempotent
    default_storage_directory()
    assert contents.check(dir=True)

    contents.remove()
    assert not contents.check()
    contents.ensure()

    with pytest.raises(OSError):
        default_storage_directory()
