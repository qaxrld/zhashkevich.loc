from controllers.site_controller import SiteController
from controllers.test_controller import TestController

routes = {
    "/home" : [SiteController, SiteController.index],
    "/about" :  [SiteController, SiteController.about],
    "/test" :  [TestController, TestController.test],
    "/test-action" :  [TestController, TestController.action],
}