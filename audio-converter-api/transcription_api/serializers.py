from rest_framework import serializers
from .models import AudioTranscription
import os


class AudioTranscriptionSerializer(serializers.ModelSerializer):
    """Serializer for AudioTranscription model"""
    
    file_size_display = serializers.CharField(read_only=True)
    processing_time_display = serializers.CharField(read_only=True)
    audio_file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = AudioTranscription
        fields = [
            'id', 'audio_file', 'original_filename', 'file_size', 'file_size_display',
            'file_format', 'transcription_text', 'status', 'processing_time',
            'processing_time_display', 'error_message', 'created_at', 'updated_at',
            'audio_file_url'
        ]
        read_only_fields = [
            'id', 'original_filename', 'file_size', 'file_size_display',
            'file_format', 'transcription_text', 'status', 'processing_time',
            'processing_time_display', 'error_message', 'created_at', 'updated_at',
            'audio_file_url'
        ]
    
    def get_audio_file_url(self, obj):
        """Return the URL for the audio file"""
        if obj.audio_file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.audio_file.url)
        return None


class AudioTranscriptionCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new audio transcription requests"""
    
    class Meta:
        model = AudioTranscription
        fields = ['audio_file']
    
    def validate_audio_file(self, value):
        """Validate the uploaded audio file"""
        # Check file size (100MB limit)
        if value.size > 100 * 1024 * 1024:  # 100MB
            raise serializers.ValidationError("File size must be less than 100MB")
        
        # Check file extension
        allowed_extensions = ['.mp3', '.wav', '.m4a', '.flac', '.ogg', '.aac', '.wma']
        file_extension = os.path.splitext(value.name)[1].lower()
        
        if file_extension not in allowed_extensions:
            raise serializers.ValidationError(
                f"Unsupported file format. Allowed formats: {', '.join(allowed_extensions)}"
            )
        
        return value


class AudioTranscriptionUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating audio transcription status"""
    
    class Meta:
        model = AudioTranscription
        fields = ['status', 'transcription_text', 'processing_time', 'error_message']
        read_only_fields = ['id', 'created_at', 'updated_at']


class AudioTranscriptionListSerializer(serializers.ModelSerializer):
    """Serializer for listing audio transcriptions (minimal data)"""
    
    file_size_display = serializers.CharField(read_only=True)
    processing_time_display = serializers.CharField(read_only=True)
    
    class Meta:
        model = AudioTranscription
        fields = [
            'id', 'original_filename', 'file_size_display', 'file_format',
            'status', 'processing_time_display', 'created_at'
        ]
