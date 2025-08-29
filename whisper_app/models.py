from django.db import models
from django.utils import timezone
import os

class AudioTranscription(models.Model):
    """Model to store audio file uploads and transcription results"""
    
    AUDIO_FORMATS = [
        ('wav', 'WAV'),
        ('mp3', 'MP3'),
        ('m4a', 'M4A'),
        ('flac', 'FLAC'),
        ('ogg', 'OGG'),
        ('aac', 'AAC'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    # File information
    audio_file = models.FileField(upload_to='audio_uploads/')
    original_filename = models.CharField(max_length=255)
    file_size = models.BigIntegerField(help_text='File size in bytes')
    file_format = models.CharField(max_length=10, choices=AUDIO_FORMATS)
    
    # Transcription results
    transcription_text = models.TextField(blank=True, null=True)
    confidence_score = models.FloatField(blank=True, null=True)
    
    # Processing information
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    processing_time = models.FloatField(blank=True, null=True, help_text='Processing time in seconds')
    error_message = models.TextField(blank=True, null=True)
    
    # Metadata
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Audio Transcription'
        verbose_name_plural = 'Audio Transcriptions'
    
    def __str__(self):
        return f"{self.original_filename} - {self.status}"
    
    def get_file_size_display(self):
        """Return human-readable file size"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if self.file_size < 1024.0:
                return f"{self.file_size:.1f} {unit}"
            self.file_size /= 1024.0
        return f"{self.file_size:.1f} TB"
    
    def get_processing_time_display(self):
        """Return human-readable processing time"""
        if self.processing_time:
            if self.processing_time < 60:
                return f"{self.processing_time:.1f} seconds"
            elif self.processing_time < 3600:
                return f"{self.processing_time / 60:.1f} minutes"
            else:
                return f"{self.processing_time / 3600:.1f} hours"
        return "N/A"
    
    def delete(self, *args, **kwargs):
        """Delete the audio file when the model instance is deleted"""
        if self.audio_file:
            if os.path.isfile(self.audio_file.path):
                os.remove(self.audio_file.path)
        super().delete(*args, **kwargs)
