from datetime import datetime, time
from rest_framework import status as http_status
from django.db import transaction
from common.decorators import RequestMethod
from common import errorcode
from app_user_account.models import UserAccount, Hobby, HobbyMapping, Interest, InterestMapping
from faker import Faker
import random
from elasticsearch import Elasticsearch
from config import sensitive

RequestMethod_ = RequestMethod()
es = Elasticsearch(hosts=sensitive.ES['hosts'], port=sensitive.ES['port'], http_auth=sensitive.ES['http_auth'])

class UserAccountFunc:
    def _get(self, user: object, input_data: dict):
        result = None
        message = {"status": None, "code": errorcode.OK, "message": None}
        result = {
            'id': user.id,
            'phone': user.phone,
            'email': user.email,
            'name': user.name,
            'gender': user.gender,
            'birthday': user.birthday,
            'picture': user.picture,
            'latitude': user.latitude,
            'longitude': user.longitude,
            'hobby': HobbyMapping.objects.filter(user=user).values_list('hobby__name', flat=True),
            'interest': InterestMapping.objects.filter(user=user).values_list('interest__name', flat=True),
            'created_at': datetime.timestamp(user.created_at),
            'updated_at': datetime.timestamp(user.updated_at),
        }
        return result, message

    def _post(self, user: object, input_data: dict):
        result = None
        message = {"status": None, "code": errorcode.OK, "message": None}
        phone = input_data.get('phone', None)
        password = input_data.get('password', None)
        user, refresh = UserAccount.objects.create_user(phone, password)
        result = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        if not user:
            message["code"] = errorcode.INTERNAL_SERVER_ERROR
            message["status"] = http_status.HTTP_500_INTERNAL_SERVER_ERROR
            message["message"] = '帳號建立失敗'
        return result, message
    
    def _put(self, user: object, input_data: dict):
        result = None
        message = {"status": None, "code": errorcode.OK, "message": None}
        hobby = input_data.get('hobby', [])
        interest = input_data.get('interest', [])
        with transaction.atomic():
            user.name = input_data.get('name', user.name)            
            user.email = input_data.get('email', user.email)
            user.gender = input_data.get('gender', user.gender)
            user.birthday = datetime.fromtimestamp(input_data.get('birthday')) if input_data.get('birthday', None) else user.birthday
            user.picture = input_data.get('picture', user.picture)
            user.latitude = input_data.get('latitude', user.latitude)
            user.longitude = input_data.get('longitude', user.longitude)
            user.updated_at = datetime.now()
            user.save()
            new_hobys = set(Hobby.objects.get_or_create(name=name)[0] for name in hobby)
            current_hobbys = set([hobby.hobby for hobby in user.hobbymapping_set.all()])
            to_remove = current_hobbys - new_hobys 
            to_add = new_hobys - current_hobbys 
            user.hobbymapping_set.filter(user=user.id, hobby__in=to_remove).delete()
            HobbyMapping.objects.bulk_create([HobbyMapping(hobby=hobby, user=user) for hobby in to_add])
            
            new_interests = set(Interest.objects.get_or_create(name=name)[0] for name in interest)
            current_interests = set([interest.interest for interest in user.interestmapping_set.all()])
            to_remove = current_interests - new_interests 
            to_add = new_interests - current_interests 
            user.interestmapping_set.filter(user=user.id, interest__in=to_remove).delete()
            InterestMapping.objects.bulk_create([InterestMapping(interest=interest, user=user) for interest in to_add])
            es_user = es.search(index='useraccount', body={
                "query": {
                    "match": {
                        "user_id": user.id
                    }
                }
            })
            body = {
                "user_id": user.id,
                "phone": user.phone,
                "email": user.email,
                "name": user.name,
                "gender": user.gender,
                "birthday": int(datetime.timestamp(user.birthday)),
                "picture": user.picture,
                "lang": {
                    "lat": user.latitude,
                    "lon": user.longitude
                },
                "hobby": list(HobbyMapping.objects.filter(user=user).values_list('hobby__name', flat=True)),
                "interest": list(InterestMapping.objects.filter(user=user).values_list('interest__name', flat=True)),
                "updated_at": int(datetime.now().timestamp())
            }
            if es_user['hits']['hits']:
                es_id = es_user["hits"]["hits"][0]["_id"]
                es.update(
                    index='useraccount', id=es_id, body={"doc": body}
                )
            else:
                body['created_at'] = int(datetime.now().timestamp())
                es.index(index='useraccount', body=body)
        return result, message
    
    def _patch(self, user: object, input_data: dict):
        result = None
        message = {"status": None, "code": errorcode.OK, "message": None}
        password = input_data.get('password', None)
        user.password = password
        user.set_password(user.password)
        user.updated_at = datetime.now()
        user.save()
        return result, message
    
    def main(self, request: object, method: str, input_data: dict):
        result, message = getattr(self, method)(request.user, input_data)
        return result, message

    @RequestMethod_.method()
    def api(self, request: object, method: str, input_data: dict):
        result, message = self.main(request, method, input_data)
        return result, message

class FakeUserAccountFunc:
    def __init__(self):
        self.fake = Faker('zh_TW')  
        self.num = 99
        
    def _post(self, user: object, input_data: dict):
        result = None
        message = {"status": None, "code": errorcode.OK, "message": None}
        phone = random.choice(['0910', '0911', '0912', '0919', '0920', '0921', '0928', '0930', '0931', '0938'])
        hobby_list = ['年齡', '距離']
        interest_list = ['閱讀', '旅行', '攝影', '烹飪', '登山', '音樂', '電影']
        for _ in range(self.num):
            profile = {
                'phone': f"{phone}-{random.randint(100, 999)}-{random.randint(100, 999)}",
                'password': self.fake.password(length=8),
                'name': self.fake.name(),
                'email': self.fake.email(),
                'gender': random.choice([0, 1]),
                'birthday': self.fake.date_of_birth(minimum_age=18, maximum_age=35),
                'picture': self.fake.image_url(),
                'latitude': round(random.uniform(25.051, 25.073), 6),
                'longitude': round(random.uniform(121.520, 121.550), 6),
                'hobby': random.sample(hobby_list, random.randint(1, 2)),
                'interest': random.sample(interest_list, random.randint(1, 5))
            }            
            user, _ = UserAccount.objects.create_user(profile['phone'], profile['password'])    
            user.name = profile['name']           
            user.email = profile['email']
            user.gender = profile['gender']
            user.birthday = profile['birthday']
            user.picture = profile['picture']
            user.latitude = profile['latitude']
            user.longitude = profile['longitude']
            user.updated_at = datetime.now()
            user.save()
            new_hobys = set(Hobby.objects.get_or_create(name=name)[0] for name in profile['hobby'])
            current_hobbys = set([hobby.hobby for hobby in user.hobbymapping_set.all()])
            to_remove = current_hobbys - new_hobys 
            to_add = new_hobys - current_hobbys 
            user.hobbymapping_set.filter(user=user.id, hobby__in=to_remove).delete()
            HobbyMapping.objects.bulk_create([HobbyMapping(hobby=hobby, user=user) for hobby in to_add])
            
            new_interests = set(Interest.objects.get_or_create(name=name)[0] for name in profile['interest'])
            current_interests = set([interest.interest for interest in user.interestmapping_set.all()])
            to_remove = current_interests - new_interests 
            to_add = new_interests - current_interests 
            user.interestmapping_set.filter(user=user.id, interest__in=to_remove).delete()
            InterestMapping.objects.bulk_create([InterestMapping(interest=interest, user=user) for interest in to_add])
            
            es_user = es.search(index='useraccount', body={
                "query": {
                    "match": {
                        "user_id": user.id
                    }
                }
            })
            body = {
                "user_id": user.id,
                "phone": user.phone,
                "email": user.email,
                "name": user.name,
                "gender": user.gender,
                "birthday": int(datetime.combine(profile['birthday'], time(0, 0)).timestamp()),
                "picture": user.picture,
                "lang": {
                    "lat": profile['latitude'],
                    "lon": profile['longitude']
                },
                "hobby": list(HobbyMapping.objects.filter(user=user).values_list('hobby__name', flat=True)),
                "interest": list(InterestMapping.objects.filter(user=user).values_list('interest__name', flat=True)),
                "updated_at": int(datetime.now().timestamp())
            }
            if es_user['hits']['hits']:
                es_id = es_user["hits"]["hits"][0]["_id"]
                es.update(
                    index='useraccount', id=es_id, body={"doc": body}
                )
            else:
                body['created_at'] = int(datetime.now().timestamp())
                es.index(index='useraccount', body=body)
        message['message'] = 'OK'
        return result, message
    
    def main(self, request: object, method: str, input_data: dict):
        result, message = getattr(self, method)(request.user, input_data)
        return result, message
    
    @RequestMethod_.method()
    def api(self, request: object, method: str, input_data: dict):
        result, message = self.main(request, method, input_data)
        return result, message
    
class ESMappingFunc:
    def _post(self, user: object, input_data: dict):
        result = None
        message = {"status": None, "code": errorcode.OK, "message": None}
        index = 'useraccount'
        body = {
            "settings": {
                "number_of_shards": 2,
                "number_of_replicas": 1,
            },
            "mappings": {
                "dynamic": "strict",
                "properties": {
                    "user_id": {"type": "integer"},
                    "phone": {"type": "keyword"},
                    "email": {"type": "keyword"},
                    "name": {"type": "keyword"},
                    "gender": {"type": "integer"},
                    "birthday": {"type": "date", "format": "epoch_second"},
                    "picture": {"type": "keyword"},
                    "lang": {"type": "geo_point"},
                    "hobby": {"type": "keyword"},
                    "interest": {"type": "keyword"},
                    "updated_at": {"type": "date", "format": "epoch_second"},
                    "created_at": {"type": "date", "format": "epoch_second"},
                }
            }
        }
        try:
            es.indices.create(index=f'a_{index}', body=body)
            es.indices.put_alias(index=f'a_{index}', name=index)
        except:
            pass
        index = 'chatroom'
        body = {
            "settings": {
                "number_of_shards": 2,
                "number_of_replicas": 1,
            },
            "mappings": {
                "dynamic": "strict",
                "properties": {
                    "chatr_room_id": {"type": "keyword"},
                    "message": {
                        "type": "nested",
                        "properties": {
                            "name": {"type": "keyword"},
                            "message": {"type": "text"},
                            "created_at": {"type": "date", "format": "epoch_second"},
                        }
                    },
                    "created_at": {"type": "date", "format": "epoch_second"},
                    "updated_at": {"type": "date", "format": "epoch_second"},
                }
            }
        }
        try:
            es.indices.create(index=f'a_{index}', body=body)
            es.indices.put_alias(index=f'a_{index}', name=index)
        except:
            pass
        message['message'] = 'OK'
        return result, message
    
    def main(self, request: object, method: str, input_data: dict):
        result, message = getattr(self, method)(request.user, input_data)
        return result, message
    
    @RequestMethod_.method()
    def api(self, request: object, method: str, input_data: dict):
        result, message = self.main(request, method, input_data)        
        return result, message      