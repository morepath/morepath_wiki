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
def index(self, request):
    return redirect(request.link(Page('FrontPage')))

with app.html(model=Page) as html:
    @html()
    def display(self, request):
        return wiki.render_page(self.name)

    @html(name='edit')
    def edit_form(self, request):
        return wiki.render_edit_form(self.name)

    @html(name='edit', request_method='POST')
    def edit(self, request):
        if request.POST.get('submit'):
            wiki.store_page(self.name, request.POST['content'])
            return redirect(request.link(self))

    @html(name='history')
    def history(self, request):
        return wiki.render_history_form(self.name)

    @html(name='history', request_method='POST')
    def revert(self, request):
        version = request.POST.get('version')
        if request.POST.get('submit') and version:
            wiki.revert_page(self.name, version)
            return redirect(request.link(self))

def main():
    morepath.autosetup()
    app.run()

if __name__ == '__main__':
    main()
