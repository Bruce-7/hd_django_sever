import requests

# 微信小程序 AppID 和 AppSecret
WX_APP_ID = '自己小程序appid'
WX_APP_SECRET = '自己小程序SECRET'

# QQ小程序 AppID 和 AppSecret
QQ_APP_ID = '自己小程序appid'
QQ_APP_SECRET = '自己小程序SECRET'


class AuthCode2SessionAPI(object):
    def __init__(self, code, provider):
        # QQ小程序服务端登录接口：
        # GET https://api.q.qq.com/sns/jscode2session?appid=APPID&secret=SECRET&js_code=JSCODE&grant_type=authorization_code

        # 微信小程序服务器登录接口：
        # GET https://api.weixin.qq.com/sns/jscode2session?appid=APPID&secret=SECRET&js_code=JSCODE&grant_type=authorization_code

        if provider == 'weixin':
            self.host = 'https://api.weixin.qq.com/sns/jscode2session'
            self.appid = WX_APP_ID
            self.secret = WX_APP_SECRET

        if provider == 'qq':
            self.host = 'https://api.q.qq.com/sns/jscode2session'
            self.appid = QQ_APP_ID
            self.secret = QQ_APP_SECRET

        self.code = code
        self.provider = provider

    def get_auth_info(self):
        url = self.host + '?appid={}&secret={}&js_code={}&grant_type=authorization_code'.format(self.appid, self.secret,
                                                                                                self.code)
        resp = requests.get(url)
        return resp.json()


if __name__ == "__main__":
    auth = AuthCode2SessionAPI('xxxxx', 'weixin')
    res = auth.get_auth_info()
    # {'session_key': 'QHo968j1SWIgor73x9DqfQ==', 'openid': 'oSE9e2Ry0oZUjshdTbZjwex3HXxA'} 正确
    # {'errcode': 40029, 'errmsg': 'invalid code, hints: [ req_id: SkbC36yFe-k3e72a ]'} 传入错误code 返回的错误
    # {'errcode': 40163, 'errmsg': 'code been used, hints: [ req_id: SkbCpAMre-mgDU.a ]'}  传入已使用的code 返回的错误
