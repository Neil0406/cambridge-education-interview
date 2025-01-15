from datetime import datetime
from rest_framework import status as http_status
from django.db import transaction
from common.decorators import RequestMethod
from app_user_account.models import InterestMapping, HobbyMapping, ChatrRoom, ChatrRoomMapping
from elasticsearch import Elasticsearch
from config import sensitive
from common import errorcode
from django.forms.models import model_to_dict

RequestMethod_ = RequestMethod()
es = Elasticsearch(hosts=sensitive.ES['hosts'], port=sensitive.ES['port'], http_auth=sensitive.ES['http_auth'])

class MatchListFunc:        
    def _get(self, user: object, input_data: dict):
        result = []
        message = {"status": None, "code": 0, "message": None}     
        distance = input_data.get('distance', 2000)
        hobbys = HobbyMapping.objects.filter(user=user).values_list('hobby__id', flat=True)
        interests = InterestMapping.objects.filter(user=user).values_list('interest__id', flat=True)        
        hobbys = list(set(HobbyMapping.objects.filter(hobby__id__in=hobbys).exclude(user=user).exclude(user__gender=user.gender).values_list('user__id', flat=True)))
        interests = list(set(InterestMapping.objects.filter(interest__id__in=interests).exclude(user=user).exclude(user__gender=user.gender).values_list('user__id', flat=True)))
        user_id_list = list(set(hobbys+interests))
        body = {
            "size": 100,
            "_source": ["user_id", "name", "gender", "birthday", "picture", "lang.lat", "lang.lon", "hobby", "interest"],
            "query": {
                "bool": {
                    "must": [
                        {
                            "terms": {
                                "user_id": user_id_list
                            }
                        },
                        {
                            "geo_distance": {
                                "distance": f"{str(distance)}m",
                                "lang.lat": user.latitude,
                                "lang.lon": user.longitude
                            }
                        }
                    ]
                }
            },
            "script_fields": {
                "distance": {
                    "script": {
                        "source": "doc['lang'].arcDistance(params.lat, params.lon)",
                        "params": {
                            "lat": user.latitude,
                            "lon": user.longitude
                        }
                    }
                }
            },
            "sort": [
                {
                    "_geo_distance": {
                        "lang": {
                            "lat": user.latitude,
                            "lon": user.longitude
                        },
                        "order": "asc",
                        "unit": "m"
                    }
                }
            ]
        }
        result = es.search(index='useraccount', body=body)['hits']['hits']
        return result, message
    
    def main(self, request: object, method: str, input_data: dict):
        result, message = getattr(self, method)(request.user, input_data)
        return result, message

    @RequestMethod_.method()
    def api(self, request: object, method: str, input_data: dict):
        result, message = self.main(request, method, input_data)
        return result, message

    
class ChatrFunc:
    def _get(self, user: object, input_data: dict):
        result = []
        message = {"status": None, "code": 0, "message": None}
        target_user_id = input_data.get('user_id', None)
        if target_user_id:
            chatr_room = ChatrRoomMapping.objects.filter(user__in=[user.id, target_user_id]).values_list('chatr_room__uuid', flat=True) 
            if chatr_room.count() != 2:
                message["code"] = errorcode.DATA_NOT_EXISTS
                message["status"] = http_status.HTTP_404_NOT_FOUND
                message["message"] = '對象不存在'
                return result, message
            if chatr_room:
                chatr_room_id = chatr_room[0]
                body = {
                    "query": {
                        "bool": {
                            "filter": [
                                {'match_phrase': {'chatr_room_id': chatr_room_id}},
                            ]
                        }
                    },
                }
                result = es.search(index='chatroom', body=body)['hits']['hits']
        return result, message

    def _post(self, user: object, input_data: dict):
        result = []
        message = {"status": None, "code": 0, "message": None}
        target_user_id = input_data.get('user_id', None)
        msg = input_data.get('message', None)
        if target_user_id:
            with transaction.atomic():
                chatr_room = ChatrRoomMapping.objects.filter(user__in=[user.id, target_user_id]).values_list('chatr_room__uuid', flat=True) 
                created_at = int(datetime.timestamp(datetime.now()))
                if chatr_room:
                    body = {
                        'query': {
                            'bool': {
                                'filter': [
                                    {'match_phrase': {'chatr_room_id': chatr_room[0]}},
                                ]
                            }
                        },
                    }
                    es_result = es.search(index='chatroom', body=body)
                    if es_result['hits']['hits']:
                        es_id = es_result["hits"]["hits"][0]["_id"]
                        if es_result["hits"]["hits"][0]['_source']['message']:
                            new_msg = es_result["hits"]["hits"][0]['_source']['message']
                            new_msg += [{"name": user.name, "message": msg, "created_at": created_at}]
                        else:
                            new_msg = [{"name": user.name, "message": msg, "created_at": created_at}]
                        es.update(
                            index='chatroom', id=es_id, body={"doc": {"message": new_msg, 'updated_at': created_at}}
                        )
                else:
                    chatr_room = ChatrRoom.objects.create()
                    ChatrRoomMapping.objects.create(chatr_room=chatr_room, user_id=user.id)
                    ChatrRoomMapping.objects.create(chatr_room=chatr_room, user_id=target_user_id)
                    body = {
                        "chatr_room_id": chatr_room.uuid,
                        "message": [
                            {
                                "name": user.name,
                                "message": msg,
                                "created_at": created_at
                            }
                        ],
                        "created_at": created_at,
                        "updated_at": created_at
                    }
                    es.index(index='chatroom', body=body)
        return result, message
    
    def main(self, request: object, method: str, input_data: dict):
        result, message = getattr(self, method)(request.user, input_data)
        return result, message

    @RequestMethod_.method()
    def api(self, request: object, method: str, input_data: dict):
        result, message = self.main(request, method, input_data)        
        return result, message
    
