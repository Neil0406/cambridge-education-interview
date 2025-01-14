from app_user_account import views
from django.urls import path

urlpatterns = [
    path('', views.UserAccount.as_view(), name='user_account'),
    path('fakeuser', views.FakeUserAccount.as_view(), name='fakeuser_account'),
    path('es_mapping', views.ESMapping.as_view(), name='es_mapping'),
]
