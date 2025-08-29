# 🎵 Audio to Text Converter

A modern web application that converts audio files to text using OpenAI's Whisper model. Built with Flask and featuring a beautiful, responsive user interface.

## ✨ Features

- **Drag & Drop Interface**: Easy file upload with drag-and-drop support
- **Multiple Audio Formats**: Supports WAV, MP3, M4A, FLAC, OGG, and AAC
- **Real-time Conversion**: Fast transcription using OpenAI Whisper
- **Modern UI**: Beautiful, responsive design that works on all devices
- **Copy to Clipboard**: One-click copying of transcription results
- **File Validation**: Automatic file type and size validation
- **Progress Indicators**: Loading states and error handling

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or download this repository**
   ```bash
   cd /path/to/your/project
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:5000`

## 📁 Project Structure

```
audio-to-text-converter/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Frontend interface
├── uploads/              # Upload directory (created automatically)
└── README.md             # This file
```

## 🔧 Configuration

### Whisper Model Selection

You can change the Whisper model size in `app.py`:

```python
# Available models: "tiny", "base", "small", "medium", "large"
model = whisper.load_model("base")  # Change this line
```

- **tiny**: Fastest, least accurate (39 MB)
- **base**: Good balance of speed/accuracy (74 MB)
- **small**: Better accuracy, slower (244 MB)
- **medium**: High accuracy, slower (769 MB)
- **large**: Best accuracy, slowest (1550 MB)

### File Size Limits

The default maximum file size is 100MB. You can modify this in `app.py`:

```python
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB
```

## 🎯 Usage

1. **Upload Audio**: Drag and drop an audio file or click to browse
2. **Select File**: Choose from supported audio formats
3. **Convert**: Click "Convert to Text" button
4. **Get Results**: View your transcription and copy to clipboard

## 📱 Supported Audio Formats

- **WAV** - Uncompressed audio
- **MP3** - Compressed audio
- **M4A** - Apple audio format
- **FLAC** - Lossless compression
- **OGG** - Open source format
- **AAC** - Advanced audio coding

## 🛠️ Development

### Running in Development Mode

```bash
python app.py
```

The app runs in debug mode by default on `http://localhost:5000`

### Production Deployment

For production use, consider:

1. **WSGI Server**: Use Gunicorn or uWSGI
2. **Environment Variables**: Set `FLASK_ENV=production`
3. **HTTPS**: Enable SSL/TLS
4. **Load Balancing**: For high traffic

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 🔍 API Endpoints

- `GET /` - Main application interface
- `POST /upload` - Audio file upload and transcription
- `GET /health` - Health check endpoint

### Upload API Response

```json
{
  "success": true,
  "transcription": "Your transcribed text here...",
  "filename": "audio_file.mp3"
}
```

## 🐛 Troubleshooting

### Common Issues

1. **Model Loading Slow**: First run downloads the Whisper model (~74MB for base)
2. **Memory Issues**: Use smaller model sizes for limited RAM
3. **File Upload Errors**: Check file format and size limits
4. **Transcription Failures**: Ensure audio file is not corrupted

### Performance Tips

- Use "tiny" or "base" models for faster processing
- Compress audio files before upload
- Close other applications to free up memory

## 📊 Performance

| Model Size | Memory Usage | Speed | Accuracy |
|------------|--------------|-------|----------|
| tiny       | ~39 MB       | Fast  | Good     |
| base       | ~74 MB       | Medium| Better   |
| small      | ~244 MB      | Slow  | High     |
| medium     | ~769 MB      | Slower| Very High|
| large      | ~1550 MB     | Slowest| Best    |

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
- **Flask** for the web framework
- **Whisper** Python library maintainers

## 📞 Support

If you encounter any issues:

1. Check the troubleshooting section above
2. Review the error logs in the terminal
3. Ensure all dependencies are properly installed
4. Verify your audio file format and size

---

**Happy Transcribing! 🎤✨**
