#!/bin/bash

echo "🎵 Starting Audio Transcription API..."
echo "====================================="

# Check if virtual environment exists
if [ ! -d "../Python/venv" ]; then
    echo "❌ Virtual environment not found. Please run from the Python directory first."
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source ../Python/venv/bin/activate

# Check if Django is installed
if ! python -c "import django" 2>/dev/null; then
    echo "❌ Django not found. Installing dependencies..."
    pip install -r requirements.txt
fi

# Check if required packages are installed
echo "🔍 Checking dependencies..."
python -c "import rest_framework, corsheaders, django_filters, drf_yasg" 2>/dev/null || {
    echo "❌ Missing required packages. Installing..."
    pip install -r requirements.txt
}

# Create media directory
mkdir -p media

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser if needed
echo "👤 Do you want to create a superuser? (y/n)"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    python manage.py createsuperuser
fi

# Start the server
echo "🚀 Starting API server on http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/swagger/"
echo "🔍 Admin Interface: http://localhost:8000/admin/"
echo "💡 Health Check: http://localhost:8000/api/health/"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python manage.py runserver 0.0.0.0:8000
