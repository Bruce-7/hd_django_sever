from rest_framework.views import APIView
from utils.response import HDResponse
from utils.clash_royale_api import ClashRoyaleAPI
from rest_framework.status import HTTP_200_OK
from rest_framework.exceptions import ValidationError


def handle_response(response):
    results = response.get('results')
    status = response.get('status')

    if status == HTTP_200_OK and results:
        return HDResponse(data_results=results, http_status=status)

    message = response.get('message')
    if not message:
        message = '皇室战争接口出错'

    return HDResponse(data_status=status, data_message=message, http_status=status)


class HomePlayersAllAPIView(APIView):
    """获取皇室战争玩家所有信息"""

    @staticmethod
    def handle_all_response(response):
        results = response.get('results')
        status = response.get('status')

        if status == HTTP_200_OK and results:
            return results

        message = response.get('message')
        if not message:
            message = '皇室战争接口出错'

        raise ValidationError(message)

    def get(self, request):
        """获取皇室战争玩家所有信息"""
        tag = self.request.query_params.get('tag')

        c_r_api = ClashRoyaleAPI()

        data_results = {}

        players = c_r_api.players(tag)
        results = self.handle_all_response(players)
        if results:
            data_results['players'] = results

        upcomingchests = c_r_api.upcomingchests(tag)
        results = self.handle_all_response(upcomingchests)
        if results:
            data_results['upcomingchests'] = results

        # battlelog = c_r_api.battlelog(tag)
        # results = self.handle_all_response(battlelog)
        # if results:
        #     data_results['battlelog'] = results

        return HDResponse(data_results=data_results, http_status=HTTP_200_OK)


class HomePlayersAPIView(APIView):
    """获取皇室战争玩家信息"""

    def get(self, request):
        """获取皇室战争玩家信息"""
        tag = self.request.query_params.get('tag')

        c_r_api = ClashRoyaleAPI()
        res = c_r_api.players(tag)

        return handle_response(res)


class HomePlayersUpcomingchestsAPIView(APIView):
    """获取皇室战争玩家即将到来的宝箱的信息"""

    def get(self, request):
        """获取皇室战争玩家即将到来的宝箱的信息"""
        tag = self.request.query_params.get('tag')

        c_r_api = ClashRoyaleAPI()
        res = c_r_api.upcomingchests(tag)
        return handle_response(res)


class HomePlayersBattlelogAPIView(APIView):
    """获取皇室战争玩家最近的战斗列表"""

    def get(self, request):
        """获取皇室战争玩家最近的战斗列表"""
        tag = self.request.query_params.get('tag')

        c_r_api = ClashRoyaleAPI()
        res = c_r_api.battlelog(tag)
        return handle_response(res)
