from django.urls import path
from . import views

app_name = 'prices'
urlpatterns = [
    path('', views.index, name='index'),
    path('json<int:pid>/', views.line_chart_json, name='json_detail'),
    path('<int:pid>/', views.line_chart, name='detail'),
    path('chart', views.line_chart, name='chart'),
    path('line_chart_json/', views.line_chart_json, name='line_chart_json')

]
