from app_main import views
from django.urls import path

urlpatterns = [
    path('match', views.MatchList.as_view(), name='match'),
    path('chatr', views.Chatr.as_view(), name='chatr'),
]
