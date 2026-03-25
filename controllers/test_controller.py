from controllers.controller import Controller

class TestController(Controller):

    def test(self, request, response):
        response.text = self.view.render_html('site/test.html', {'title' : 'тест',
                                                                            'h1' : 'Тестовая страница'})

    def action(self, request, response):
        response.text = self.view.render_html('site/action.html', {'title': 'действия',
                                                                      'h1': 'Информация о действии'})
