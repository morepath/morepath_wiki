from morepath import redirect
import morepath
import storage

wiki = storage.Storage('contents')

app = morepath.App()

@app.path(path='')
class Root(object):
    pass

class Page(object):
    def __init__(self, name):
        self.name = name

@app.path(model=Page, path='{name}')
def get_page(name):
    if not storage.wikiname_re.match(name):
        return None
    return Page(name)

@app.html(model=Root)
def index(request, model):
    return redirect(request.link(Page('FrontPage')))

with app.html(model=Page) as html:
    @html()
    def display(request, model):
        return wiki.render_page(model.name)

    @html(name='edit')
    def edit_form(request, model):
        return wiki.render_edit_form(model.name)

    @html(name='edit', request_method='POST')
    def edit(request, model):
        if request.form.get('submit'):
            wiki.store_page(model.name, request.form['content'])
            return redirect(request.link(model))

    @html(name='history')
    def history(request, model):
        return wiki.render_history_form(model.name)

    @html(name='history', request_method='POST')
    def revert(request, model):
        version = request.form.get('version')
        if request.form.get('submit') and version:
            wiki.revert_page(model.name, version)
            return redirect(request.link(model))

def main():
    morepath.autosetup()
    app.run()

if __name__ == '__main__':
    main()
