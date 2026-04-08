from controllers.articles_controller import ArticlesController
from controllers.site_controller import SiteController
from controllers.test_controller import TestController
from controllers.users_controller import UsersController
routes = {
    r"^/article/(\d+)/delete$": [ArticlesController, ArticlesController.delete],
    r"^/articles/add$": [ArticlesController, ArticlesController.add],
    r"^/article/(\d+)/edit$" : [ArticlesController, ArticlesController.edit],
    r"^/article/(\d+)$" : [ArticlesController, ArticlesController.view],
    r"^/articles$": [ArticlesController, ArticlesController.index],
    r"^/user/register$": [UsersController, UsersController.sign_up],
    r"^/user/login$": [UsersController, UsersController.sign_in],
    r"^/user/logout$": [UsersController, UsersController.logout],
    r"^/home$" : [SiteController, SiteController.index],
    r"^/about$" :  [SiteController, SiteController.about],
    r"^/test$" :  [TestController, TestController.test],
    r"^/test-action$" :  [TestController, TestController.action],
    r"^/hello/(.*)$": [SiteController, SiteController.hello],}
