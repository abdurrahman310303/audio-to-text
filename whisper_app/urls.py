from django.urls import path
from . import views

app_name = 'whisper_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_audio, name='upload_audio'),
    path('history/', views.transcription_history, name='history'),
    path('detail/<int:transcription_id>/', views.transcription_detail, name='detail'),
    path('health/', views.health_check, name='health'),
]
