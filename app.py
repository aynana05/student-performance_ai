from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add parent directory to path to import predictor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from predictor import StudentPerformancePredictor
import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    predictor = StudentPerformancePredictor()
    logger.info("✓ AI/ML System initialized")
except Exception as e:
    logger.error(f"✗ Failed to initialize: {e}")
    predictor = None

@app.route('/')
def home():
    return jsonify({
        'project': 'Student Performance AI/ML System',
        'type': 'Artificial Intelligence & Machine Learning',
        'model': 'Logistic Regression',
        'status': 'operational',
        'endpoints': {
            'POST /predict': 'Make AI prediction',
            'GET /predictions': 'Get all predictions',
            'GET /statistics': 'Get statistics'
        }
    })

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if not predictor:
            return jsonify({'error': 'AI system not initialized'}), 500
        
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        required = predictor.features
        missing = [f for f in required if f not in data]
        
        if missing:
            return jsonify({
                'error': 'Missing required features',
                'missing': missing
            }), 400
        
        prediction = predictor.predict(data)
        predictor.save_prediction(data, prediction)
        
        logger.info(f"Prediction: {prediction['predicted_score']} ({prediction['category']})")
        
        return jsonify({
            'success': True,
            'prediction': prediction,
            'input': data
        }), 200
        
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/predictions', methods=['GET'])
def get_predictions():
    try:
        predictions = predictor.get_all_predictions()
        return jsonify({
            'success': True,
            'count': len(predictions),
            'predictions': predictions
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/statistics', methods=['GET'])
def get_statistics():
    try:
        stats = predictor.get_statistics()
        return jsonify({
            'success': True,
            'statistics': stats
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    logger.info("="*60)
    logger.info("Starting AI/ML Student Performance System")
    logger.info("="*60)
    app.run(debug=True, host='0.0.0.0', port=5000)