"""clashroyalecampsite_sever URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views¡¡
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path, include
from django.views import static
from django.conf import settings
import xadmin  # xadmin后台管理
from xadmin.plugins import xversion
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

xadmin.autodiscover()
xversion.register_models()  # xversion模块自动注册需要控制的版本Model（方便数据回滚）
#  换成自己的API文档配置
schema_view = get_schema_view(
   openapi.Info(
      title="皇室营地 API",
      default_version='v1',
      description="皇室营地 所有API接口说明",
      terms_of_service="https://api.xxx.com/",
      contact=openapi.Contact(email="100000@qq.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.IsAdminUser,),
)

urlpatterns = [
    # 配置使用xadmin后台管理
    path('admin/', xadmin.site.urls),


    # 配置接口文档（三者样式，选择一个就行）
    # re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('docs/', schema_view.with_ui('redoc', cache_timeout=0), name='docs'),


    # users URL
    path('user/', include(('users.urls', 'users'), namespace='users')),


    # home URL
    path('', include(('home.urls', 'home'), namespace='home')),


    # 静态文件和媒体文件
    re_path(r'^static/(?P<path>.*)$', static.serve,
            {'document_root': settings.STATIC_ROOT}, name='static'),
    re_path(r'^media/(?P<path>.*)$', static.serve,
            {'document_root': settings.MEDIA_ROOT}, name='media'),
]
