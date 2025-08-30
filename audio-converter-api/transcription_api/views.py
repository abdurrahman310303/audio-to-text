import os
import time
import logging
from django.conf import settings
from rest_framework import status, generics, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from .models import AudioTranscription
from .serializers import (
    AudioTranscriptionSerializer,
    AudioTranscriptionCreateSerializer,
    AudioTranscriptionListSerializer
)

logger = logging.getLogger(__name__)
whisper_model = None

def load_whisper_model():
    global whisper_model
    if whisper_model is None:
        try:
            import whisper
            model_name = getattr(settings, 'WHISPER_MODEL_NAME', 'base')
            whisper_model = whisper.load_model(model_name)
            logger.info(f"Whisper model loaded successfully!")
        except Exception as e:
            logger.error(f"Error loading Whisper model: {e}")
            raise
    return whisper_model

class AudioTranscriptionCreateView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            serializer = AudioTranscriptionCreateSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            audio_file = request.FILES.get('audio_file')
            if not audio_file:
                return Response({'error': 'No audio file provided'}, status=status.HTTP_400_BAD_REQUEST)
            
            transcription = AudioTranscription.objects.create(
                audio_file=audio_file,
                original_filename=audio_file.name,
                file_size=audio_file.size,
                file_format=os.path.splitext(audio_file.name)[1][1:].lower()
            )
            
            self.process_transcription(transcription)
            
            result_serializer = AudioTranscriptionSerializer(transcription, context={'request': request})
            return Response(result_serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"Error creating transcription: {e}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def process_transcription(self, transcription):
        try:
            transcription.status = 'processing'
            transcription.save()
            
            start_time = time.time()
            model = load_whisper_model()
            result = model.transcribe(transcription.audio_file.path)
            
            processing_time = time.time() - start_time
            
            transcription.transcription_text = result['text']
            transcription.status = 'completed'
            transcription.processing_time = processing_time
            transcription.save()
            
        except Exception as e:
            processing_time = time.time() - start_time if 'start_time' in locals() else 0
            transcription.status = 'failed'
            transcription.error_message = str(e)
            transcription.processing_time = processing_time
            transcription.save()

class AudioTranscriptionListView(generics.ListAPIView):
    queryset = AudioTranscription.objects.all()
    serializer_class = AudioTranscriptionListSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'file_format']
    search_fields = ['original_filename']
    ordering_fields = ['created_at', 'updated_at', 'file_size', 'processing_time']
    ordering = ['-created_at']

class AudioTranscriptionDetailView(generics.RetrieveAPIView):
    queryset = AudioTranscription.objects.all()
    serializer_class = AudioTranscriptionSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    try:
        load_whisper_model()
        return Response({
            'status': 'healthy',
            'message': 'Audio transcription API is running',
            'whisper_model': 'loaded'
        })
    except Exception as e:
        return Response({
            'status': 'unhealthy',
            'message': 'Audio transcription API has issues',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def api_info(request):
    return Response({
        'name': 'Audio Transcription API',
        'version': '1.0.0',
        'description': 'REST API for converting audio files to text using OpenAI Whisper',
        'endpoints': {
            'upload': '/api/transcriptions/',
            'list': '/api/transcriptions/list/',
            'detail': '/api/transcriptions/{id}/',
            'health': '/api/health/',
            'info': '/api/info/'
        },
        'supported_formats': ['mp3', 'wav', 'm4a', 'flac', 'ogg', 'aac', 'wma'],
        'max_file_size': '100MB'
    })
