import hashlib
from django.conf import settings
from db.base_model import BaseModel
from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    """自定义jwt token"""

    refresh = RefreshToken.for_user(user)

    return {
        'token_refresh': str(refresh),
        'token': str(refresh.access_token),
    }


class User(AbstractUser, BaseModel):
    """用户信息"""

    PROVIDER_TYPE = [
        ['weixin', '微信'],
        ['qq', 'QQ']
    ]

    GENDER_TYPE = [
        ['male', '男'],
        ['female', '女']
    ]

    openid = models.CharField(verbose_name='微信或QQ的OpenID', help_text='微信或者QQ服务器返回的用户唯一标识',
                              max_length=100, unique=True, null=True, blank=True)
    name = models.CharField(verbose_name='姓名', help_text='姓名', max_length=20, null=True, blank=True)
    gender = models.CharField(verbose_name='性别', help_text='性别', max_length=6,
                              choices=GENDER_TYPE, default='female', null=True, blank=True)
    mobile = models.CharField(verbose_name='电话', help_text='电话', max_length=11, null=True, blank=True)
    avatar_url = models.ImageField(verbose_name='头像URL', help_text='头像URL', upload_to='user/avatar',
                                   default='user/avatar/default.png', null=True, blank=True)
    birthday = models.DateField(verbose_name='生日', help_text='生日', null=True, blank=True)
    provider = models.CharField(verbose_name='供应商', help_text='登录的平台是哪家供应商', choices=PROVIDER_TYPE,
                                max_length=20, default='weixin', null=False, blank=False)
    mini_program_avatar_url = models.CharField(verbose_name='小程序头像URL', help_text='小程序头像URL', max_length=500, null=True, blank=True)

    class Meta:
        db_table = 't_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        # 对象的一个易于理解的名称，为单数：verbose_name
        # 该对象复数形式的名称：verbose_name_plural，如果此项没有设置，Django 会使用 verbose_name + "s"

    def __str__(self):
        return self.username  # 返回admin管理页展示信息（一般选择关键信息）

    @property
    def token(self):
        """
        token：认证令牌
        token_refresh：用于刷新认证令牌
        """
        return get_tokens_for_user(self)

    def create_username_password(self):
        # 没有账号和密码，通过openid自动创建
        if not self.username and not self.password and self.openid:
            b_key = settings.SECRET_KEY.encode(encoding="utf-8")
            b_openid = self.openid.encode(encoding="utf-8")
            self.username = hashlib.pbkdf2_hmac('sha256', b_openid, b_key, 10).hex()

            b_username = self.username.encode(encoding="utf-8")
            self.password = hashlib.pbkdf2_hmac('sha256', b_username, b_openid, 10).hex()

    def save(self, *args, **kwargs):
        self.create_username_password()

        if self.username and self.password:
            super().save(*args, **kwargs)
