#!/bin/bash
# Start the CRM Chatbot Flask server

cd "$(dirname "$0")"
source venv/bin/activate

echo "Starting CRM Chatbot API server..."
echo "Server will be available at http://localhost:5001"
echo "Press Ctrl+C to stop the server"
echo ""

python app.py

