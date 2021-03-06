import tornado.web
import os
from wigi.Handlers.MainHandler import MainHandler
from wigi.Handlers.ItemHandler import ItemHandler
from wigi.Handlers.LoginHandler import LoginHandler
from wigi.conf.config import getConfiguration 
from tornado.options import options, define

#get configuration data
site_config = getConfiguration()

define("port", default=int(site_config.get('tornado_settings','tornado_server_port')), help="run on the given port", type=int)
define("facebook_api_key", help="your Facebook application API key",
       default=site_config.get('wigi','facebook_api_key'))
define("facebook_secret", help="your Facebook application secret",
       default=site_config.get('wigi','facebook_secret'))
define("media_dir", default="media/", help="location of media directory relative to project.")

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/login", LoginHandler),
            (r"/([0-9]+)/items", ItemHandler),
        ]
        settings = dict(
                        cookie_secret=site_config.get('tornado_settings','cookie_secret'),
                        login_url="/login",
                        template_path=os.path.join(os.path.dirname(__file__), "templates"),
                        static_path=os.path.join(os.path.dirname(__file__), "static"),
                        facebook_api_key=options.facebook_api_key,
                        facebook_secret=options.facebook_secret,
                        debug=site_config.get('tornado_settings','debug'),
                        xsrf_cookies=site_config.getboolean('tornado_settings','xsrf_cookies'),                                
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        
        
