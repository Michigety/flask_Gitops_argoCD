from flask import Flask, jsonify
from datetime import datetime
import os

app = Flask(__name__)

def get_version():
    """VERSION 파일에서 버전 정보를 읽어옴"""
    try:
        with open("VERSION", "r") as f:
            return f.read().strip()
    except Exception:
        return "unknown"

@app.route('/health')
def health_check():
    """헬스 체크 엔드포인트"""
    health_data = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "flask-health-check",
        "version": get_version(),
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
