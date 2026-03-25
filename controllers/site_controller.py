
from controllers.controller import Controller
from services.db import Db

class SiteController(Controller):

    def index(self, request, response):
        db = Db()
        items = db.query("SELECT * FROM 'articles'")
        print(items)
        response.text = self.view.render_html('site/index.html', {'title' : 'MVC фреймворк',
                                                                            'h1' : 'Главная страница'})

    def about(self, request, response):
        response.text = self.view.render_html('site/about.html', {'title'  : 'MVC фреймворк - о нас',
                                                                                'h1' : 'О нас'})
    def hello(self, request, response, user_name):
        response.text = self.view.render_html('site/hello.html', {'title'  : 'MVC фреймворк - приветствие',
                                                                                'h1' : 'привет!',
                                                                                'user' : user_name})


