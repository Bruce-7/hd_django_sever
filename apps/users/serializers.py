from abc import ABCMeta, ABC

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from . import models
from utils.auth_code2Session import AuthCode2SessionAPI


class UserLoginSerializer(serializers.ModelSerializer):
    """用户登录序列化"""

    # 选项参数：
    # max_length 最大长度
    # min_length 最小长度
    # allow_blank 是否允许为空
    # trim_whitespace 是否截断空白字符
    # max_value 最小值
    # min_value 最大值
    #
    # 通项参数：
    # read_only 该字段仅用于序列化输出，默认false
    # write_only 该字段仅用于反序列化输入，默认false
    # required 该字段在反序列化时必须输入，默认true
    # default 反序列化时使用的默认值
    # allow_null 该字段是否允许传入None，默认false
    # validators 该字段使用的验证器
    # error_messages 包含错误编号与错误信息的字典
    # label 用于HTML展示页面时，显示的字段名称
    # help_text 用于HTML展示页面时，显示的字段帮助提示信息

    code = serializers.CharField(label='code', help_text='小程序登录授权code码', write_only=True,
                                 max_length=100, min_length=1, required=True,
                                 error_messages={
                                     'invalid': '不是有效的字符串',
                                     'null': 'code参数不能为空',
                                     'blank': 'code参数内容不能为空',
                                     'required': '不能缺少code字段',
                                     'max_length': 'code码太长',
                                     'min_length': 'code码太短'
                                 }, )

    def validate(self, attrs):
        code = attrs.pop('code')
        provider = attrs.get('provider')
        auth_info = AuthCode2SessionAPI(code, provider).get_auth_info()
        openid = auth_info.get('openid', None)

        if not openid:
            raise ValidationError('code码无效')

        attrs['openid'] = openid
        self.instance = models.User.objects.filter(openid=openid).first()  # view使用save情况，没有就创建用户否则更新用户信息
        return attrs

    class Meta:
        model = models.User
        fields = ['code', 'provider', 'id', 'name', 'gender', 'mobile', 'avatar_url', 'birthday',
                  'mini_program_avatar_url', 'token']
        # read_only_fields = ['id', 'name', 'gender', 'mobile', 'avatar_url', 'birthday', 'provider', 'token']
        # exclude = [] 刨除某些字段
        # depth = 1 跨表自动深度（展示外键所有字段）
        extra_kwargs = {
            'provider': {
                'required': True,
                'write_only': True,
                'error_messages': {
                    'invalid': '不是有效的字符串',
                    'null': 'provider参数不能为空',
                    'blank': 'provider参数内容不能为空',
                    'required': '不能缺少provider字段',
                    'invalid_choice': '正确传入合法平台供应商'
                }
            },
            'name': {
                'error_messages': {
                    'invalid': '不是有效的字符串',
                    'max_length': '名字太长'
                }
            },
            'gender': {
                'error_messages': {
                    'invalid': '不是有效的字符串',
                    'invalid_choice': '正确传入合法平台供应商'
                }
            },
            'mini_program_avatar_url': {
                'error_messages': {
                    'invalid': '不是有效的字符串',
                    'max_length': 'URL头像链接太长'
                }
            },
            'id': {
                'read_only': True,
            },
            'token': {
                'read_only': True,
            },
            'avatar_url': {
                'read_only': True,
            },
            'birthday': {
                'read_only': True,
            },
            'mobile': {
                'read_only': True,
            },
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'name', 'gender', 'mobile', 'avatar_url', 'birthday', 'mini_program_avatar_url']


class TokenRefreshSerializer(serializers.Serializer):
    """token刷新序列化"""

    token_refresh = serializers.CharField(label='token_refresh', help_text='刷新得到最新访问token，旧token_refresh使用后不能再使用',
                                          write_only=True, max_length=500, min_length=1, required=True,
                                          error_messages={
                                              'invalid': '不是有效的字符串',
                                              'null': 'token_refresh参数不能为空',
                                              'blank': 'token_refresh参数内容不能为空',
                                              'required': '不能缺少token_refresh字段',
                                              'max_length': '内容太长',
                                              'min_length': '内容太短'
                                          }, )

    def validate(self, attrs):
        try:
            refresh = RefreshToken(attrs['token_refresh'])
        except Exception as err:
            raise ValidationError('无效的token_refresh内容')

        data = {'token': str(refresh.access_token)}
        refresh.blacklist()  # 将使用的token_refresh加入黑名单，旧值只能刷新一次。
        refresh.set_jti()
        refresh.set_exp()
        data['token_refresh'] = str(refresh)

        return data
