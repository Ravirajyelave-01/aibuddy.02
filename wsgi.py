"""
Production-ready WSGI server for Flask app
Install: pip install gunicorn
Run: gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
"""
from app import app, socketio

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000)
