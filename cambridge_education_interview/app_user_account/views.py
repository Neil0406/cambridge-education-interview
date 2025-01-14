from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from common.decorators import InputCheck
from common.helperfunc import api_response
from common import errorcode
from app_user_account.functions import UserAccountFunc, FakeUserAccountFunc, ESMappingFunc

input_check = InputCheck(SystemName="app_user_account")

UserAccountFunc_ = UserAccountFunc()
FakeUserAccountFunc_ = FakeUserAccountFunc()
ESMappingFunc_ = ESMappingFunc()

# User帳號
class UserAccount(APIView):
    
    permission_classes = (IsAuthenticated,)
    required_data = []
    @input_check.key_check(required_data)
    @swagger_auto_schema(
        operation_summary='用戶資料',
        operation_description='',
        responses = {'200': openapi.Response(
            description = 'message',
            examples={
                'application/json':{
                    "result": [],
                    "code": 0
                }
            }
        )}
    )
    def get(self, request, input_data, router):
        '''
        param:
            必填欄位：
                -
            非必填欄位：
                -
        '''
        result, message = UserAccountFunc_.api(request, input_data)
        return api_response(result, **message)
    
    permission_classes = (AllowAny,)
    required_data = ['phone', 'password']
    @input_check.key_check(required_data)
    @swagger_auto_schema(
        operation_summary='新增帳號 -> jwt',
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
				'phone': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='電話 ex: 0912-345-678'
				),
				'password': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='密碼'
				)
			}
		)
    )
    def post(self, request, input_data, router):
        '''
        param:
            必填欄位：
                phone, password
            非必填欄位：
                -
        '''
        result, message = UserAccountFunc_.api(request, input_data)
        return api_response(result, **message)
    
    permission_classes = (IsAuthenticated,)
    required_data = ['name', 'email', 'gender', 'birthday', 'picture', 'latitude', 'longitude', 'hobby', 'interest']
    @input_check.key_check(required_data)
    @swagger_auto_schema(
        operation_summary='更新帳號',
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
				'name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='姓名'
				),
				'email': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Email'
				),
				'gender': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='性別 1: 男 0: 女'
				),
				'birthday': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='生日 (timestamp)'
				),
                'picture': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='照片'
                ),
                'latitude': openapi.Schema(
                    type=openapi.TYPE_NUMBER,
                    description='緯度'
                ),
                'longitude': openapi.Schema(
                    type=openapi.TYPE_NUMBER,
                    description='經度'
                ),
                'hobby': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    description='偏好',
                    items=openapi.Items(
                        type=openapi.TYPE_STRING,
                        description='偏好'
                    )
                ),
                'interest': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    description='興趣',
                    items=openapi.Items(
                        type=openapi.TYPE_STRING,
                        description='興趣'
                    )
                ),
			}
		)
    )
    def put(self, request, input_data, router):
        '''
        param:
            必填欄位：
                name, email, gender, birthday, picture, latitude, longitude, hobby, interest
            非必填欄位：
                -
        '''
        result, message = UserAccountFunc_.api(request, input_data)
        return api_response(result, **message)
    
    permission_classes = (IsAuthenticated,)
    required_data = ['password']
    @input_check.key_check(required_data)
    @swagger_auto_schema(
        operation_summary='更新密碼',
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
				'password': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='密碼'
				)
			}
		)
    )
    def patch(self, request, input_data, router):
        '''
        param:
            必填欄位：
                password
            非必填欄位：
                -
        '''
        result, message = UserAccountFunc_.api(request, input_data)
        return api_response(result, **message)

# FakeUser帳號新增
class FakeUserAccount(APIView):
    permission_classes = (IsAdminUser,)
    
    required_data = []
    @input_check.key_check(required_data)
    @swagger_auto_schema(
        operation_summary='FakeUser帳號',
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
        )}
    )
    def post(self, request, input_data, router):
        '''
        param:
            必填欄位：
                -
            非必填欄位：
                -
        '''
        result, message = FakeUserAccountFunc_.api(request, input_data)
        return api_response(result, **message)

# ES mapping
class ESMapping(APIView):
    permission_classes = (IsAdminUser,)
    
    required_data = []
    @input_check.key_check(required_data)
    @swagger_auto_schema(
        operation_summary='ES mapping',
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
        )}
    )
    def post(self, request, input_data, router):
        '''
        param:
            必填欄位：
                -
            非必填欄位：
                -
        '''
        result, message = ESMappingFunc_.api(request, input_data)        
        return api_response(result, **message)