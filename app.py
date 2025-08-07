from flask import Flask, jsonify
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/health')
def health_check():
    """헬스 체크 엔드포인트"""
    health_data = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "flask-health-check",
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development")
    }
    return jsonify(health_data), 200

@app.route('/')
def home():
    """루트 엔드포인트"""
    return jsonify({
        "message": "Flask Health Check API",
        "endpoints": {
            "health": "/health"
        }
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
