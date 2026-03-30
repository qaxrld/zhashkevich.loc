from controllers.articles_controller import ArticlesController
from controllers.site_controller import SiteController
from controllers.test_controller import TestController

routes = {
    r"^/article/(\d+)$" : [ArticlesController, ArticlesController.view],
    r"^/articles$": [ArticlesController, ArticlesController.index],
    r"^/home$" : [SiteController, SiteController.index],
    r"^/about$" :  [SiteController, SiteController.about],
    r"^/test$" :  [TestController, TestController.test],
    r"^/test-action$" :  [TestController, TestController.action],
    r"^/hello/(.*)$": [SiteController, SiteController.hello],

}