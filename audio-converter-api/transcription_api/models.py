from django.db import models
from django.utils import timezone
import os


class AudioTranscription(models.Model):
    """Model for storing audio transcription requests and results"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    AUDIO_FORMATS = [
        ('mp3', 'MP3'),
        ('wav', 'WAV'),
        ('m4a', 'M4A'),
        ('flac', 'FLAC'),
        ('ogg', 'OGG'),
        ('aac', 'AAC'),
        ('wma', 'WMA'),
    ]
    
    # File information
    audio_file = models.FileField(upload_to='audio_uploads/')
    original_filename = models.CharField(max_length=255)
    file_size = models.BigIntegerField(help_text='File size in bytes')
    file_format = models.CharField(max_length=10, choices=AUDIO_FORMATS)
    
    # Transcription results
    transcription_text = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Processing metadata
    processing_time = models.FloatField(blank=True, null=True, help_text='Processing time in seconds')
    error_message = models.TextField(blank=True, null=True)
    
    # Timestamps
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
        if self.processing_time is None:
            return "N/A"
        if self.processing_time < 60:
            return f"{self.processing_time:.2f}s"
        minutes = int(self.processing_time // 60)
        seconds = self.processing_time % 60
        return f"{minutes}m {seconds:.2f}s"
    
    def delete(self, *args, **kwargs):
        """Override delete to remove the audio file from storage"""
        if self.audio_file:
            if os.path.isfile(self.audio_file.path):
                os.remove(self.audio_file.path)
        super().delete(*args, **kwargs)
