import os
import time
import logging
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from .models import AudioTranscription
import whisper

# Configure logging
logger = logging.getLogger(__name__)

# Initialize Whisper model (load once at startup)
whisper_model = None

def load_whisper_model():
    """Load the Whisper model - this can take some time on first run"""
    global whisper_model
    if whisper_model is None:
        logger.info("Loading Whisper model...")
        whisper_model = whisper.load_model("base")  # You can change to "tiny", "small", "medium", "large"
        logger.info("Whisper model loaded successfully!")
    return whisper_model

def index(request):
    """Main page view"""
    return render(request, 'whisper_app/index.html')

@csrf_exempt
@require_http_methods(["POST"])
def upload_audio(request):
    """Handle audio file upload and transcription"""
    try:
        if 'audio' not in request.FILES:
            return JsonResponse({'error': 'No audio file provided'}, status=400)
        
        audio_file = request.FILES['audio']
        if audio_file.name == '':
            return JsonResponse({'error': 'No file selected'}, status=400)
        
        # Validate file type
        allowed_extensions = {'.wav', '.mp3', '.m4a', '.flac', '.ogg', '.aac'}
        file_ext = os.path.splitext(audio_file.name)[1].lower()
        if file_ext not in allowed_extensions:
            return JsonResponse({'error': 'Invalid file type'}, status=400)
        
        # Create transcription record
        transcription = AudioTranscription.objects.create(
            original_filename=audio_file.name,
            file_size=audio_file.size,
            file_format=file_ext[1:],  # Remove the dot
            status='processing'
        )
        
        # Save the file
        file_path = default_storage.save(f'audio_uploads/{transcription.id}_{audio_file.name}', audio_file)
        transcription.audio_file = file_path
        transcription.save()
        
        # Process with Whisper
        start_time = time.time()
        model = load_whisper_model()
        
        logger.info(f"Transcribing audio file: {audio_file.name}")
        
        # Get the full file path
        full_file_path = os.path.join(settings.MEDIA_ROOT, file_path)
        
        # Transcribe the audio
        result = model.transcribe(full_file_path)
        transcription_text = result["text"]
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Update transcription record
        transcription.transcription_text = transcription_text
        transcription.processing_time = processing_time
        transcription.status = 'completed'
        transcription.save()
        
        logger.info(f"Transcription completed for {audio_file.name} in {processing_time:.2f}s")
        
        return JsonResponse({
            'success': True,
            'transcription': transcription_text,
            'filename': audio_file.name,
            'processing_time': processing_time,
            'transcription_id': transcription.id
        })
        
    except Exception as e:
        logger.error(f"Error during transcription: {str(e)}")
        
        # Update transcription record with error
        if 'transcription' in locals():
            transcription.status = 'failed'
            transcription.error_message = str(e)
            transcription.save()
        
        return JsonResponse({'error': f'Transcription failed: {str(e)}'}, status=500)

def transcription_history(request):
    """View to display transcription history"""
    transcriptions = AudioTranscription.objects.all()[:50]  # Limit to last 50
    return render(request, 'whisper_app/history.html', {'transcriptions': transcriptions})

def transcription_detail(request, transcription_id):
    """View to display detailed transcription information"""
    try:
        transcription = AudioTranscription.objects.get(id=transcription_id)
        return render(request, 'whisper_app/detail.html', {'transcription': transcription})
    except AudioTranscription.DoesNotExist:
        return JsonResponse({'error': 'Transcription not found'}, status=404)

def health_check(request):
    """Health check endpoint"""
    return JsonResponse({
        'status': 'healthy',
        'model_loaded': whisper_model is not None,
        'django_version': '5.2.5'
    })
