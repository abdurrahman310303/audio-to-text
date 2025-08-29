import os
import tempfile
import whisper
from flask import Flask, request, render_template, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'wav', 'mp3', 'm4a', 'flac', 'ogg', 'aac'}

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize Whisper model (load once at startup)
model = None

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def load_whisper_model():
    """Load the Whisper model - this can take some time on first run"""
    global model
    if model is None:
        logger.info("Loading Whisper model...")
        model = whisper.load_model("base")  # You can change to "tiny", "small", "medium", "large"
        logger.info("Whisper model loaded successfully!")
    return model

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    file = request.files['audio']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        try:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
                file.save(temp_file.name)
                temp_path = temp_file.name
            
            # Load Whisper model and transcribe
            model = load_whisper_model()
            logger.info(f"Transcribing audio file: {file.filename}")
            
            # Transcribe the audio
            result = model.transcribe(temp_path)
            transcription = result["text"]
            
            # Clean up temporary file
            os.unlink(temp_path)
            
            logger.info(f"Transcription completed for {file.filename}")
            return jsonify({
                'success': True,
                'transcription': transcription,
                'filename': file.filename
            })
            
        except Exception as e:
            logger.error(f"Error during transcription: {str(e)}")
            # Clean up temporary file if it exists
            if 'temp_path' in locals():
                try:
                    os.unlink(temp_path)
                except:
                    pass
            return jsonify({'error': f'Transcription failed: {str(e)}'}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'model_loaded': model is not None})

if __name__ == '__main__':
    # Load the model when starting the app
    load_whisper_model()
    app.run(debug=True, host='0.0.0.0', port=5000)
