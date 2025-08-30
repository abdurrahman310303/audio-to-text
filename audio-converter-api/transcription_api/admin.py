from django.contrib import admin
from .models import AudioTranscription


@admin.register(AudioTranscription)
class AudioTranscriptionAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'original_filename', 'file_format', 'file_size_display',
        'status', 'processing_time_display', 'created_at'
    ]
    list_filter = ['status', 'file_format', 'created_at']
    search_fields = ['original_filename', 'transcription_text']
    readonly_fields = [
        'id', 'created_at', 'updated_at', 'file_size_display',
        'processing_time_display'
    ]
    
    fieldsets = (
        ('File Information', {
            'fields': ('audio_file', 'original_filename', 'file_size', 'file_format')
        }),
        ('Transcription Results', {
            'fields': ('transcription_text', 'status', 'processing_time', 'error_message')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def file_size_display(self, obj):
        return obj.get_file_size_display()
    file_size_display.short_description = 'File Size'
    
    def processing_time_display(self, obj):
        return obj.get_processing_time_display()
    processing_time_display.short_description = 'Processing Time'
    
    actions = ['retry_failed_transcriptions']
    
    def retry_failed_transcriptions(self, request, queryset):
        """Retry failed transcriptions"""
        failed_transcriptions = queryset.filter(status='failed')
        count = 0
        
        for transcription in failed_transcriptions:
            try:
                transcription.status = 'pending'
                transcription.error_message = ''
                transcription.save()
                count += 1
            except Exception as e:
                self.message_user(
                    request,
                    f"Error retrying transcription {transcription.id}: {e}",
                    level='ERROR'
                )
        
        if count > 0:
            self.message_user(
                request,
                f"Successfully queued {count} failed transcriptions for retry."
            )
    
    retry_failed_transcriptions.short_description = "Retry failed transcriptions"
