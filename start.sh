#!/bin/bash

echo "🎵 Starting Audio to Text Converter..."
echo "======================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python3 -m venv venv"
    echo "Then run: source venv/bin/activate && pip install -r requirements_django.txt"
    exit 1
fi

# Activate virtual environment
echo "🚀 Activating virtual environment..."
source venv/bin/activate

# Check if Django is installed
if ! python -c "import django" 2>/dev/null; then
    echo "❌ Django not found!"
    echo "Please install Django: pip install -r requirements_django.txt"
    exit 1
fi

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser if needed
echo "👤 Creating superuser (if needed)..."
echo "You can create an admin user to manage transcriptions."
echo "Run: python manage.py createsuperuser"

# Start Django development server
echo "📱 Starting Django application on port 8000..."
echo "🌐 Open your browser and go to: http://localhost:8000"
echo "🔧 Admin panel: http://localhost:8000/admin"
echo "⏹️  Press Ctrl+C to stop the application"
echo "=============================================="

python manage.py runserver 0.0.0.0:8000
