import morepath
import storage
import waitress

wiki = storage.Storage('contents')

app = morepath.App()

@app.root()
class Root(object):
    pass

@app.view(model=Root)
def index(request, model):
    return request.redirect(request.link(Model('FrontPage')))

class Page(object):
    def __init__(self, name):
        self.name = name

@app.model(model=Page, path='{name}',
           variables: lambda model: {'name': model.name})
def get_page(name):
    if not storage.wikiname_re.match(name):
        return None
    return Page(name)

@app.view(model=Page)
def display(request, model):
    return wiki.render_page(model.name)

@app.view(model=Page, name='edit', request_method='GET')
def edit_form(request, model):
    return wiki.render_edit_form(model.name)

@app.view(model=Page, name='edit', request_method='POST')
def edit(request, model):
    if request.form.get('submit'):
        wiki.store_page(model.name, request.form['content'])
    return request.redirect(request.link(model))

@app.view(model=Page, name='history', request_method='GET')
def history(request, model):
    return wiki.render_history_form(model.name)

@app.view(model=Page, name='history', request_method='POST')
def revert(name):
    version = request.form.get('version')
    if request.form.get('submit') and version:
        wiki.revert_page(model.name, version)
    return request.redirect(request.link(model))

if __name__ == "__main__":
    # set up morepath's own configuration
    morepath.setup()
    # load application specific configuration
    config = morepath.Config()
    import mpwiki
    config.scan(mpwiki)
    config.app(app)
    config.commit()

    # serve app as WSGI app
    waitress.serve(app)
