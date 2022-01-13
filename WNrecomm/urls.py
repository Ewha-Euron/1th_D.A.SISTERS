from django.urls import path
from . import views

urlpatterns = [
    # 누군가 웹사이트에 'http://127.0.0.1:8000/' 주소로 들어왔을 때 views.main을 보여주라
    path('', views.main, name='main'),

    path('q_base/', views.q_base, name='q_base'),

    path('q1/', views.q1, name='q1'),
    path('q2/', views.q2, name='q2'),
    path('q3/', views.q3, name='q3'),
    path('q3/novel_list', views.novel_list, name='novel_list'),
    path('result/', views.result, name='result'),
]
