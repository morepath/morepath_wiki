from morepath import redirect

from .model import Root, Page
from .app import App


@App.html(model=Root)
def index(self, request):
    return redirect(request.link(Page('FrontPage')))

with App.html(model=Page) as html:
    @html()
    def display(self, request):
        return request.app.wiki.render_page(self.name)

    @html(name='edit')
    def edit_form(self, request):
        return request.app.wiki.render_edit_form(self.name)

    @html(name='edit', request_method='POST')
    def edit(self, request):
        if request.POST.get('submit'):
            request.app.wiki.store_page(self.name, request.POST['content'])
            return redirect(request.link(self))
        elif request.POST.get('cancel'):
            return redirect(request.link(Page('FrontPage')))

    @html(name='history')
    def history(self, request):
        return request.app.wiki.render_history_form(self.name)

    @html(name='history', request_method='POST')
    def revert(self, request):
        version = request.POST.get('version')
        if request.POST.get('submit') and version:
            request.app.wiki.revert_page(self.name, version)
            return redirect(request.link(self))
        elif request.POST.get('cancel') or not version:
            return redirect(request.link(Page('FrontPage')))
