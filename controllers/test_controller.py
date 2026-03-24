from views.view import View

class TestController:
    def __init__(self):
        self.layout = "default"
        self.view =  View(self.layout)

    def test(self, request, response):
        response.text = self.view.render_html('site/test.html', {'title' : 'тест',
                                                                            'h1' : 'Тестовая страница'})

    def action(self, request, response):
        response.text = self.view.render_html('site/action.html', {'title': 'действия',
                                                                      'h1': 'Информация о действии'})
