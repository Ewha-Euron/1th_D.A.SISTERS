from django.urls import path
from . import views

urlpatterns = [
    # 누군가 웹사이트에 'http://127.0.0.1:8000/' 주소로 들어왔을 때 views.main을 보여주라
    path('', views.main, name='main'),

    path('q1/', views.q1, name='q1'),
    path('result/', views.result, name='result'),
]
