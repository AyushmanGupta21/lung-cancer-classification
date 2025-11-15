"""
Lung Cancer Classification - Flask Backend API
Professional REST API for histopathological image analysis
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow import keras
import io
import os
import time
from datetime import datetime

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

# Configuration
MODEL_PATH = 'best_lung_model.h5'
IMG_SIZE = (150, 150)
CLASS_NAMES = ['Adenocarcinoma', 'Normal', 'Squamous Cell Carcinoma']

# Class information
CLASS_INFO = {
    'Adenocarcinoma': {
        'emoji': '🔴',
        'color': '#FF6B6B',
        'description': 'A type of non-small cell lung cancer that begins in mucus-secreting cells.',
        'action': 'Immediate consultation with oncologist recommended.',
        'severity': 'high'
    },
    'Squamous Cell Carcinoma': {
        'emoji': '🟠',
        'color': '#FF8C42',
        'description': 'A type of non-small cell lung cancer that begins in flat cells lining the airways.',
        'action': 'Immediate consultation with oncologist recommended.',
        'severity': 'high'
    },
    'Normal': {
        'emoji': '🟢',
        'color': '#51CF66',
        'description': 'Healthy lung tissue with no signs of malignancy.',
        'action': 'No immediate action required. Continue regular monitoring.',
        'severity': 'low'
    }
}

# Global model variable
model = None

print("=" * 60)
print("FLASK SERVER STARTING")
print("=" * 60)
print(f"Python version: {tf.version.VERSION}")
print(f"TensorFlow version: {tf.__version__}")
print(f"Starting at: {datetime.now()}")
print("=" * 60)


def load_model_once():
    """Load the model once when server starts"""
    global model
    
    if model is not None:
        return model
    
    print(f"\n{'='*60}")
    print(f"LOADING MODEL")
    print(f"{'='*60}")
    
    try:
        # Check if model exists
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")
        
        # Get model size
        model_size = os.path.getsize(MODEL_PATH) / (1024 * 1024)
        print(f"Model file size: {model_size:.2f} MB")
        
        # Load model with Keras 3.x compatibility
        print(f"Loading model...")
        start_time = time.time()
        
        try:
            # Try with safe_mode=False (Keras 3.x)
            model = keras.models.load_model(MODEL_PATH, compile=False, safe_mode=False)
            print(f"✓ Loaded with safe_mode=False")
        except:
            # Fallback without safe_mode
            model = keras.models.load_model(MODEL_PATH, compile=False)
            print(f"✓ Loaded without safe_mode")
        
        load_time = time.time() - start_time
        print(f"Model loaded in {load_time:.2f} seconds")
        print(f"Input shape: {model.input_shape}")
        print(f"Output shape: {model.output_shape}")
        
        # Recompile
        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        print(f"✓ Model compiled and ready!")
        print(f"{'='*60}\n")
        
        return model
        
    except Exception as e:
        print(f"❌ ERROR loading model: {str(e)}")
        print(f"{'='*60}\n")
        return None


@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('static', 'index.html')


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/predict', methods=['POST'])
def predict():
    """Prediction endpoint"""
    try:
        # Check if model is loaded
        if model is None:
            return jsonify({
                'error': 'Model not loaded',
                'success': False
            }), 500
        
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({
                'error': 'No file uploaded',
                'success': False
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'error': 'No file selected',
                'success': False
            }), 400
        
        # Read and process image
        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes))
        
        # Convert RGBA to RGB if needed
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        
        # Get original dimensions
        original_width, original_height = img.size
        
        # Resize image
        img_resized = img.resize(IMG_SIZE)
        
        # Convert to array
        img_array = np.array(img_resized, dtype=np.float32)
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        # Normalize
        img_array = img_array / 255.0
        
        # Predict
        start_time = time.time()
        predictions = model.predict(img_array, verbose=0)
        prediction_time = time.time() - start_time
        
        # Get results
        predicted_class_idx = int(np.argmax(predictions[0]))
        predicted_class = CLASS_NAMES[predicted_class_idx]
        confidence = float(predictions[0][predicted_class_idx] * 100)
        
        # All probabilities
        probabilities = {
            CLASS_NAMES[i]: float(predictions[0][i] * 100)
            for i in range(len(CLASS_NAMES))
        }
        
        # Get class info
        class_info = CLASS_INFO[predicted_class]
        
        # Build response
        response = {
            'success': True,
            'predicted_class': predicted_class,
            'confidence': round(confidence, 2),
            'probabilities': {k: round(v, 2) for k, v in probabilities.items()},
            'class_info': class_info,
            'prediction_time': round(prediction_time, 3),
            'image_info': {
                'original_width': original_width,
                'original_height': original_height,
                'format': img.format if img.format else 'Unknown'
            },
            'timestamp': datetime.now().isoformat()
        }
        
        print(f"✓ Prediction: {predicted_class} ({confidence:.2f}%) in {prediction_time:.3f}s")
        
        return jsonify(response)
        
    except Exception as e:
        print(f"❌ Prediction error: {str(e)}")
        return jsonify({
            'error': str(e),
            'success': False
        }), 500


@app.route('/api/model-info', methods=['GET'])
def model_info():
    """Get model information"""
    if model is None:
        return jsonify({
            'error': 'Model not loaded',
            'success': False
        }), 500
    
    try:
        return jsonify({
            'success': True,
            'model_info': {
                'input_shape': str(model.input_shape),
                'output_shape': str(model.output_shape),
                'total_params': int(model.count_params()),
                'classes': CLASS_NAMES,
                'image_size': IMG_SIZE
            }
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500


if __name__ == '__main__':
    # Load model before starting server
    print("\n🚀 Initializing server...")
    model = load_model_once()
    
    if model is None:
        print("❌ Failed to load model. Server will not start.")
        exit(1)
    
    print("\n✅ Server ready to accept requests!")
    print("=" * 60)
    print("Access the application at: http://localhost:5000")
    print("=" * 60)
    
    # Start Flask server
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
