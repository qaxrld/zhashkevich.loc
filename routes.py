from controllers.articles_controller import ArticlesController
from controllers.site_controller import SiteController
from controllers.test_controller import TestController
from controllers.users_controller import UsersController
from controllers.api.articles_api_controller import ArticlesApiController
from controllers.api.users_api_controller import UsersApiController


routes = {
    r"^/article/(\d+)/delete$": [ArticlesController, {"POST": ArticlesController.delete}],
    r"^/articles/add$": [ArticlesController, ArticlesController.add],
    r"^/article/(\d+)/edit$": [ArticlesController, ArticlesController.edit],
    r"^/article/(\d+)$": [ArticlesController, ArticlesController.view],
    r"^/articles$": [ArticlesController, ArticlesController.index],
    r"^/user/register$": [UsersController, UsersController.sign_up],
    r"^/user/login$": [UsersController, UsersController.sign_in],
    r"^/user/logout$": [UsersController, UsersController.logout],
    r"^/home$": [SiteController, SiteController.index],
    r"^/about$": [SiteController, SiteController.about],
    r"^/test$": [TestController, TestController.test],
    r"^/test-action$": [TestController, TestController.action],
    r"^/hello/(.*)$": [SiteController, SiteController.hello],
    r"^/api/article/(\d+)$": [
        ArticlesApiController, {"GET": ArticlesApiController.view}
    ],
    r"^/api/articles/?$": [
        ArticlesApiController, {
            "GET": ArticlesApiController.index,
            "POST": ArticlesApiController.add,
        }
    ],
    r"^/api/articles/(\d+)/delete$": [
        ArticlesApiController, {"DELETE": ArticlesApiController.delete}
    ],
    r"^/api/articles/(\d+)$": [
        ArticlesApiController, {
            "GET": ArticlesApiController.view,
            "PUT": ArticlesApiController.edit,
            "PATCH": ArticlesApiController.edit,
            "DELETE": ArticlesApiController.delete,
        }
    ],
    r"^/api/user$": [
        UsersApiController, {"GET": UsersApiController.user}
    ],
    r"^/api/user/login$": [
        UsersApiController, {"POST": UsersApiController.login}
    ],
}
