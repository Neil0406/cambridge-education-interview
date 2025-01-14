from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from common.decorators import InputCheck
from common.helperfunc import api_response
from common import errorcode
from app_main.functions import MatchListFunc, ChatrFunc

input_check = InputCheck(SystemName="app_main")

MatchListFunc_ = MatchListFunc()
ChatrFunc_ = ChatrFunc()

# 用戶配對列表
class MatchList(APIView):
    permission_classes = (IsAuthenticated,)
    
    required_data = []
    @input_check.key_check(required_data)
    @swagger_auto_schema(
        operation_summary='用戶配對列表',
        operation_description='',
        responses = {'200': openapi.Response(
            description = 'message',
            examples={
                'application/json':{
                    "result": [
                    ],
                    "code": 0
                }
            }            
        )},
        manual_parameters=[
            openapi.Parameter(
                name='distance',
                in_=openapi.IN_QUERY,
                description='距離（公尺M）',
                type=openapi.TYPE_INTEGER,
                required = False,
                default = 2000,
            )
        ]
    )
    def get(self, request, input_data, router):
        '''
        param:
            必填欄位：
                - 
            非必填欄位：
                - distance
        '''
        result, message = MatchListFunc_.api(request, input_data)
        return api_response(result, **message)
    
# 聊天功能
class Chatr(APIView):
    permission_classes = (IsAuthenticated,)
    
    required_data = ["user_id"]
    @input_check.key_check(required_data)
    @swagger_auto_schema(
        operation_summary='取得訊息',
        operation_description='',
        responses = {'200': openapi.Response(
            description = 'message',
            examples={
                'application/json':{
                    "result": [
                    ],
                    "code": 0
                }
            }            
        )},
        manual_parameters = [
            openapi.Parameter(
                name='user_id',
                in_=openapi.IN_QUERY,
                description='對象ID',
                type=openapi.TYPE_INTEGER,
                required = True,
            )
        ]
    )
    def get(self, request, input_data, router):
        '''
        param:
            必填欄位：
                - user_id
            非必填欄位：
                -
        '''
        result, message = ChatrFunc_.api(request, input_data)
        return api_response(result, **message)
        
    required_data = ["user_id"]
    @input_check.key_check(required_data)
    @swagger_auto_schema(
        operation_summary='發送訊息',
        operation_description='',
        responses = {'200': openapi.Response(
            description = 'message',
            examples={
                'application/json':{
                    "result": [
                    ],
                    "code": 0
                }
            }            
        )},
        request_body=openapi.Schema(
			type=openapi.TYPE_OBJECT,
			required=required_data,
			properties={
				'user_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='對象ID'
				),
                'message': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='訊息'
                )
			}
		)
    )
    def post(self, request, input_data, router):
        '''
        param:
            必填欄位：
                - user_id, message
            非必填欄位：
                -
        '''
        result, message = ChatrFunc_.api(request, input_data)
        return api_response(result, **message)
