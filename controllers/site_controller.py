class SiteController:
    def index(self, request, response):
        response.text = '''
        <!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>home</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>

<header class="bg-dark text-white py-3">
    <div class="container d-flex justify-content-between align-items-center">
        <h1 class="h4 m-0">Мой сайт</h1>
        <nav>
            <a href="#" class="text-white me-3">Главная</a>
            <a href="#" class="text-white me-3">О нас</a>
            <a href="#" class="text-white">Контакты</a>
        </nav>
    </div>
</header>

<main class="container my-5">
    <p>Здесь основной контент страницы</p>
</main>
<footer class="bg-light text-center py-3 mt-auto">
    <div class="container">
        <p class="mb-0">© 2026 Мой сайт</p>
    </div>
</footer>

</body>
</html>

        '''

    def about(self, request, response):
        response.text = "Страница о нас"