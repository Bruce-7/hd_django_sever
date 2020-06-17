import json
import requests
import urllib.parse
from django.conf import settings
from rest_framework.exceptions import ValidationError


class ClashRoyaleAPI(object):
    """皇室战争API"""

    def __init__(self):
        # 'Accept': '*/*' 默认
        self.host = 'https://api.clashroyale.com/v1'
        if settings.DEBUG:
            self.headers = {
                'Accept': 'application/json',
                'Authorization': 'Bearer xxx'}
        else:
            self.headers = {
                'Accept': 'application/json',
                'Authorization': 'Bearer xxx'}

    @staticmethod
    def validate(player_tag):
        if not player_tag.startswith('#'):
            raise ValidationError('玩家标签格式不对')

    @staticmethod
    def handle_response(response):
        message = None

        if response.text:
            result_json = json.loads(response.text)
        else:
            message = '皇室战争接口出错啦'

        if message:
            return {'message': message, 'status': response.status_code}
        return {'results': result_json, 'status': response.status_code}

    # 获取玩家相关API
    def upcomingchests(self, player_tag):
        """获取有关皇室战争玩家即将到来的宝箱的信息"""

        self.validate(player_tag)
        url_player_tag = urllib.parse.quote(player_tag)
        url = self.host + '/players/{}/upcomingchests/'.format(url_player_tag)
        response = requests.get(url, headers=self.headers)
        return self.handle_response(response)

    def players(self, player_tag):
        """获取皇室战争玩家信息"""

        self.validate(player_tag)
        url_player_tag = urllib.parse.quote(player_tag)
        url = self.host + '/players/{}/'.format(url_player_tag)
        response = requests.get(url, headers=self.headers)
        return self.handle_response(response)

    def battlelog(self, player_tag):
        """获取皇室战争玩家最近的战斗列表"""

        self.validate(player_tag)
        url_player_tag = urllib.parse.quote(player_tag)
        url = self.host + '/players/{}/battlelog/'.format(url_player_tag)
        response = requests.get(url, headers=self.headers)
        return self.handle_response(response)

    # 获取部落相关API

    # 获取卡组相关API

    # 获取比赛相关API

    # 获取排名相关API

    # 获取锦标赛相关API


if __name__ == "__main__":
    c_r_api = ClashRoyaleAPI()
    res = c_r_api.upcomingchests('#xxx')
