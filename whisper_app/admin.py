from django.contrib import admin
from django.utils.html import format_html
from .models import AudioTranscription

@admin.register(AudioTranscription)
class AudioTranscriptionAdmin(admin.ModelAdmin):
    list_display = [
        'original_filename', 
        'file_format', 
        'file_size_display', 
        'status', 
        'processing_time_display',
        'created_at'
    ]
    
    list_filter = [
        'status', 
        'file_format', 
        'created_at'
    ]
    
    search_fields = [
        'original_filename', 
        'transcription_text'
    ]
    
    readonly_fields = [
        'created_at', 
        'updated_at', 
        'processing_time', 
        'file_size'
    ]
    
    fieldsets = (
        ('File Information', {
            'fields': ('audio_file', 'original_filename', 'file_format', 'file_size')
        }),
        ('Transcription Results', {
            'fields': ('transcription_text', 'confidence_score'),
            'classes': ('collapse',)
        }),
        ('Processing Information', {
            'fields': ('status', 'processing_time', 'error_message'),
            'classes': ('collapse',)
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
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()
    
    def has_add_permission(self, request):
        # Only allow viewing and editing, not manual creation
        return False
    
    actions = ['retry_failed_transcriptions']
    
    def retry_failed_transcriptions(self, request, queryset):
        failed_transcriptions = queryset.filter(status='failed')
        count = failed_transcriptions.count()
        
        for transcription in failed_transcriptions:
            transcription.status = 'pending'
            transcription.error_message = ''
            transcription.save()
        
        self.message_user(
            request, 
            f'Successfully queued {count} failed transcriptions for retry.'
        )
    
    retry_failed_transcriptions.short_description = 'Retry failed transcriptions'
    
    class Media:
        css = {
            'all': ('admin/css/whisper_admin.css',)
        }
