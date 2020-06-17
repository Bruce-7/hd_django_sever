from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from utils.response import HDResponse
from .serializers import UserLoginSerializer, UserSerializer, TokenRefreshSerializer
from . import models


class CustomBackend(ModelBackend):
    """自定义用户验证"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(models.User.USERNAME_FIELD)
        if username is None or password is None:
            return

        # noinspection PyBroadException
        try:
            # 添加了一个支持手机验证
            user = models.User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as err:
            return None


class TokenRefreshGenericAPIView(GenericAPIView):
    """token刷新"""

    authentication_classes = []
    permission_classes = []
    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        """
        使用token_refresh刷新得到最新访问token
        token_refresh使用后不能再使用
        """
        token_deserializer = self.get_serializer(data=request.data)
        token_deserializer.is_valid(raise_exception=True)
        return HDResponse(data_results=token_deserializer.validated_data, http_status=status.HTTP_201_CREATED)


class UserLoginGenericAPIView(GenericAPIView):
    """用户登录"""

    authentication_classes = []
    permission_classes = []
    queryset = models.User.objects.filter(is_delete=False)
    serializer_class = UserLoginSerializer
    # lookup_field = 'pk'  # 先定义好，单查可以使用，默认是pk，自定义主键的有名分组，如果路由有名分组不是pk，这个属性就要自己设置了。

    def post(self, request, *args, **kwargs):
        """
        用户登录（并生成对应小程序的用户）
        """
        user_login_deserializer = self.get_serializer(data=request.data)  # 反序列化
        user_login_deserializer.is_valid(raise_exception=True)  # 校验数据

        user = user_login_deserializer.save()  # 没有就创建用户否则更新用户信息
        user_serializer = self.get_serializer(user)  # 序列化

        return HDResponse(data_results=user_serializer.data, http_status=status.HTTP_201_CREATED)


class UserGenericAPIView(GenericViewSet, RetrieveModelMixin):
    """用户信息"""

    permission_classes = [IsAuthenticated]
    queryset = models.User.objects.filter(is_delete=False)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        """获取用户信息"""
        instance = self.get_object()
        user_serializer = self.get_serializer(instance)
        return HDResponse(data_results=user_serializer.data, http_status=status.HTTP_200_OK)


class UserTestGenericAPIView(GenericAPIView):
    """用户test"""

    queryset = models.User.objects.filter(is_delete=False)

    def get(self, request, *args, **kwargs):
        """
        用户登录
        """

        return HDResponse(data_results={'get': '测试'}, http_status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        用户登录
        """

        return HDResponse(data_results={'post': '测试'}, http_status=status.HTTP_201_CREATED)

