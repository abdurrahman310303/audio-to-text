from django.urls import path
from . import views

app_name = 'transcription_api'

urlpatterns = [
    # Main API endpoints
    path('transcriptions/', views.AudioTranscriptionCreateView.as_view(), name='create'),
    path('transcriptions/list/', views.AudioTranscriptionListView.as_view(), name='list'),
    path('transcriptions/<int:id>/', views.AudioTranscriptionDetailView.as_view(), name='detail'),
    
    # Utility endpoints
    path('health/', views.health_check, name='health'),
    path('info/', views.api_info, name='info'),
]
