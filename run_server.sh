#!/bin/bash

echo "Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "Failed to activate virtual environment"
    exit 1
fi

echo "Starting Django development server..."
python manage.py runserver