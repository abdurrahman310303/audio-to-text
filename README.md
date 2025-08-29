# 🎵 Audio to Text Converter - Django Edition

A modern, production-ready Django web application that converts audio files to text using OpenAI's Whisper model. Built with Django 5.2+ and featuring a beautiful, responsive user interface with database storage, admin management, and complete transcription history.

## ✨ What We've Built

### 🎯 **Core Application**
- **Django Backend**: Robust, scalable web framework with proper MVC architecture
- **Audio Transcription**: OpenAI Whisper integration for high-quality speech-to-text conversion
- **Database Storage**: SQLite database with Django ORM for transcription history
- **Admin Interface**: Built-in Django admin for transcription management
- **File Management**: Automatic file storage, validation, and cleanup

### 🎨 **User Interface**
- **Modern Design**: Beautiful, responsive web interface that works on all devices
- **Drag & Drop**: Intuitive file upload with drag-and-drop support
- **Real-time Processing**: Live status updates and progress indicators
- **History View**: Complete transcription history with search and filtering
- **Detail Pages**: Comprehensive transcription information and results

### 🔧 **Technical Features**
- **Multiple Audio Formats**: WAV, MP3, M4A, FLAC, OGG, AAC support
- **File Validation**: Automatic format and size validation
- **Error Handling**: Comprehensive error handling and user feedback
- **Performance**: Optimized for speed with configurable Whisper models
- **Security**: CSRF protection, file type validation, and secure uploads

## 🏗️ Architecture & How It Works

### 📁 **Project Structure**
```
audio-to-text-converter/
├── audio_converter/          # Django project settings
│   ├── settings.py           # Django configuration
│   ├── urls.py              # Main URL routing
│   └── wsgi.py              # WSGI configuration
├── whisper_app/             # Main Django app
│   ├── models.py            # Database models
│   ├── views.py             # Business logic & API endpoints
│   ├── admin.py             # Admin interface configuration
│   └── urls.py              # App URL patterns
├── templates/               # HTML templates
│   └── whisper_app/
│       ├── base.html        # Base template with navigation
│       ├── index.html       # Main upload interface
│       ├── history.html     # Transcription history table
│       └── detail.html      # Transcription details page
├── static/                  # CSS, JavaScript, images
│   ├── css/style.css        # Modern, responsive styling
│   └── js/main.js          # Interactive functionality
└── media/                   # Uploaded audio files
```

### 🔄 **How It Works**

#### 1. **File Upload Process**
```
User Uploads Audio → File Validation → Database Record → Whisper Processing → Result Storage
```

- **File Upload**: User drags & drops or selects audio file
- **Validation**: Checks file type, size, and format
- **Database**: Creates `AudioTranscription` record with status 'pending'
- **Processing**: Sends file to OpenAI Whisper model
- **Storage**: Saves transcription result and updates status

#### 2. **Whisper Integration**
```python
# Load Whisper model (cached for performance)
model = whisper.load_model("base")  # Configurable: tiny, base, small, medium, large

# Process audio file
result = model.transcribe(audio_file_path)
transcription_text = result["text"]
```

#### 3. **Database Models**
```python
class AudioTranscription(models.Model):
    # File information
    audio_file = models.FileField(upload_to='audio_uploads/')
    original_filename = models.CharField(max_length=255)
    file_size = models.BigIntegerField()
    file_format = models.CharField(max_length=10)
    
    # Transcription results
    transcription_text = models.TextField()
    confidence_score = models.FloatField(null=True)
    
    # Processing status
    status = models.CharField(choices=STATUS_CHOICES)
    processing_time = models.FloatField()
    error_message = models.TextField(null=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

#### 4. **API Endpoints**
- `GET /` - Main upload interface
- `POST /upload/` - Audio file upload and transcription
- `GET /history/` - Transcription history page
- `GET /detail/<id>/` - Individual transcription details
- `GET /health/` - System health check
- `GET /admin/` - Django admin interface

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- ffmpeg (for audio processing)

### Installation

1. **Clone or download this repository**
   ```bash
   cd /path/to/your/project
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install ffmpeg**
   ```bash
   # macOS
   brew install ffmpeg
   
   # Ubuntu/Debian
   sudo apt update && sudo apt install ffmpeg
   
   # Windows
   choco install ffmpeg
   ```

5. **Run the application**
   ```bash
   ./start.sh
   ```

6. **Open your browser**
   - Main app: `http://localhost:8000`
   - Admin panel: `http://localhost:8000/admin`

### First Time Setup

1. **Create admin user**
   ```bash
   python manage.py createsuperuser
   ```

2. **Access admin panel**
   - Go to `http://localhost:8000/admin`
   - Login with your superuser credentials
   - Manage transcriptions, users, and system settings

## 🎯 How to Use

### 📱 **Web Interface**

1. **Upload Audio**
   - Drag and drop an audio file onto the upload area
   - Or click to browse and select a file
   - Supported formats: WAV, MP3, M4A, FLAC, OGG, AAC

2. **Convert to Text**
   - Click "Convert to Text" button
   - Watch the progress indicator
   - View real-time processing status

3. **Get Results**
   - Copy transcription to clipboard
   - Save to history for later access
   - Download as text file

### 📚 **History & Management**

1. **View History**
   - Click "History" in navigation
   - See all transcriptions with status, format, and timing
   - Filter by status, format, or date

2. **Transcription Details**
   - Click "View" on any completed transcription
   - See file information, processing details, and full text
   - Copy or download transcription results

3. **Admin Management**
   - Access Django admin at `/admin`
   - View, edit, and manage all transcriptions
   - Retry failed transcriptions
   - Monitor system performance

## 🔧 Configuration & Customization

### Whisper Model Selection

Edit `whisper_app/views.py` to change the model:

```python
# Available models with different trade-offs
model = whisper.load_model("tiny")    # 39 MB  - Fast, good accuracy
model = whisper.load_model("base")    # 74 MB  - Balanced speed/accuracy
model = whisper.load_model("small")   # 244 MB - Better accuracy, slower
model = whisper.load_model("medium")  # 769 MB - High accuracy, slower
model = whisper.load_model("large")   # 1550 MB- Best accuracy, slowest
```

### File Upload Limits

Modify `audio_converter/settings.py`:

```python
# Maximum file upload size (default: 100MB)
DATA_UPLOAD_MAX_MEMORY_SIZE = 100 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 100 * 1024 * 1024
```

### Database Configuration

Change database in `audio_converter/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 📊 Features & Capabilities

### 🎵 **Audio Support**
- **Formats**: WAV, MP3, M4A, FLAC, OGG, AAC
- **Quality**: High-quality transcription with configurable models
- **Size**: Up to 100MB file uploads (configurable)
- **Languages**: Multi-language support via Whisper

### 💾 **Data Management**
- **Storage**: Automatic file storage with cleanup
- **History**: Complete transcription history
- **Search**: Find transcriptions by filename or content
- **Export**: Download transcriptions as text files
- **Admin**: Full administrative control

### 🎨 **User Experience**
- **Responsive**: Works on desktop, tablet, and mobile
- **Drag & Drop**: Intuitive file upload interface
- **Real-time**: Live status updates and progress
- **Error Handling**: Clear error messages and recovery
- **Accessibility**: Keyboard navigation and screen reader support

## 🚀 Production Deployment

### WSGI Server
```bash
pip install gunicorn
gunicorn audio_converter.wsgi:application -w 4 -b 0.0.0.0:8000
```

### Environment Variables
Create `.env` file:
```bash
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@localhost/dbname
```

### Production Settings
Update `settings.py`:
```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
SECRET_KEY = os.environ.get('SECRET_KEY')

# Static files
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

## 🔍 API Reference

### Upload Endpoint
```http
POST /upload/
Content-Type: multipart/form-data

Form Data:
- audio: Audio file (WAV, MP3, M4A, FLAC, OGG, AAC)

Response:
{
  "success": true,
  "transcription": "Your transcribed text here...",
  "filename": "audio_file.mp3",
  "processing_time": 2.45,
  "transcription_id": 123
}
```

### Health Check
```http
GET /health/

Response:
{
  "status": "healthy",
  "model_loaded": true,
  "django_version": "5.2.5"
}
```

## 🐛 Troubleshooting

### Common Issues

1. **ffmpeg not found**
   ```bash
   # Install ffmpeg for your operating system
   brew install ffmpeg  # macOS
   sudo apt install ffmpeg  # Ubuntu/Debian
   ```

2. **Model loading slow**
   - First run downloads Whisper model (~74MB for base)
   - Use smaller models for faster startup
   - Check internet connection

3. **File upload errors**
   - Verify file format is supported
   - Check file size limits
   - Ensure proper permissions

4. **Database errors**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

### Performance Tips

- Use "tiny" or "base" models for faster processing
- Compress audio files before upload
- Close other applications to free up memory
- Use PostgreSQL for better performance with large datasets

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **OpenAI** for the Whisper model
- **Django** for the web framework
- **Whisper** Python library maintainers

## 📞 Support

If you encounter any issues:

1. Check the troubleshooting section above
2. Review the Django error logs
3. Ensure all dependencies are properly installed
4. Verify your audio file format and size
5. Check the database migrations are applied

---

**Your Django audio-to-text conversion app is now ready for production use! 🎤✨**

Built with ❤️ using Django, OpenAI Whisper, and modern web technologies.
