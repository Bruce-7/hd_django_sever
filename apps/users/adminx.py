import xadmin
from . import models
from django.utils.translation import ugettext as _
from xadmin.plugins.auth import UserAdmin, Main, Fieldset, Side, Row


class BaseAdmin(object):
    """xadmin的基本配置"""

    enable_themes = True  # 开启主题切换功能
    use_bootswatch = True


class CommAdmin(object):
    """xadmin的全局配置"""

    site_title = "皇室营地后台"  # 设置站点标题
    site_footer = "皇室营地"  # 设置底部关于版权信息
    # menu_style = "accordion"  # 设置菜单折叠


class UserProfileAdmin(UserAdmin):
    """用户信息的配置"""

    list_display = ['username', 'is_staff', 'is_superuser', 'is_active', 'openid', 'name', 'provider']  # 要显示的字段
    search_fields = ['name', 'mobile', 'provider']  # 搜索的字段
    ordering = ['create_time', ]

    change_user_password_template = None
    style_fields = {'user_permissions': 'm2m_transfer'}
    model_icon = 'fa fa-user'
    relfield_style = 'fk-ajax'

    def get_form_layout(self):
        self.form_layout = (
            Main(
                Fieldset(_('基础信息'),
                         'openid', 'username', 'password'),
                Fieldset(_('个人信息'),
                         Row('first_name', 'last_name'),
                         'name', 'gender', 'avatar_url', 'birthday', 'provider', 'create_time', 'update_time',
                         'is_delete',
                         ),
                Fieldset(_('联络信息'),
                         Row('email', 'mobile')),
                Fieldset(_('登录信息'),
                         Row('last_login', 'date_joined')),
            ),
            Side(
                Fieldset(_('权限信息'),
                         'is_active', 'is_staff', 'is_superuser'
                         ),
            )
        )
        return super(UserAdmin, self).get_form_layout()


xadmin.site.register(xadmin.views.BaseAdminView, BaseAdmin)
xadmin.site.register(xadmin.views.CommAdminView, CommAdmin)

xadmin.site.unregister(models.User)
xadmin.site.register(models.User, UserProfileAdmin)
