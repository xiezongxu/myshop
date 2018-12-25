__author__='derek'

import xadmin
from xadmin import views
from .models import VerifyCode


class BaseSetting(object):
    enable_themes=True
    use_bootswatch=True


class GlobalSettings(object):
    site_title='cms2'
    site_footer='http://www.baidu.com'

    menu_style='accordion'

class VerfyCoderAdmin(object):
    list_display=['code','mobile','add_time']

xadmin.site.register(VerifyCode,VerfyCoderAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSettings)