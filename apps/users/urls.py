from django.urls import path, re_path
from . import views


urlpatterns = [
    path('login/', views.UserLoginGenericAPIView.as_view(), name='login'),
    path('token/refresh/', views.TokenRefreshGenericAPIView.as_view(), name='token_refresh'),
    re_path(r'^(?P<pk>\d+)/$', views.UserGenericAPIView.as_view({'get': 'retrieve'}), name='user'),
    path('test/', views.UserTestGenericAPIView.as_view(), name='test')
]
