from controllers.articles_controller import ArticlesController
from controllers.site_controller import SiteController
from controllers.test_controller import TestController
from controllers.users_controller import UsersController
from controllers.api.articles_api_controller import ArticlesApiController
routes = {
    r"^/article/(\d+)/delete$": [ArticlesController, ArticlesController.delete],
    r"^/articles/add$": [ArticlesController, ArticlesController.add],
    r"^/article/(\d+)/edit$" : [ArticlesController, ArticlesController.edit],
    r"^/article/(\d+)$" : [ArticlesController, ArticlesController.view],
    r"^/articles$": [ArticlesController, ArticlesController.index],
    r"^/user/register$": [UsersController, UsersController.sign_up],
    r"^/user/login$": [UsersController, UsersController.sign_in],
    # r"^/users$": [UsersController, UsersController.users],
    r"^/user/logout$": [UsersController, UsersController.logout],
    r"^/home$" : [SiteController, SiteController.index],
    r"^/about$" :  [SiteController, SiteController.about],
    r"^/test$" :  [TestController, TestController.test],
    r"^/test-action$" :  [TestController, TestController.action],
    r"^/hello/(.*)$": [SiteController, SiteController.hello],
    r"^/api/article/(\d+)$": [ArticlesApiController, ArticlesApiController.view],
    r"^/api/articles/?$": [ArticlesApiController, ArticlesApiController.index],
    }
