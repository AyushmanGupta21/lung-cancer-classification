# 🫁 Lung Cancer Classification AI

Advanced deep learning system for histopathological image analysis using Convolutional Neural Networks.

## 🎯 Overview

This project provides a professional medical-grade web interface for classifying lung cancer from histopathological images into three categories:
- **Adenocarcinoma** - Non-small cell lung cancer beginning in mucus-secreting cells
- **Squamous Cell Carcinoma** - Non-small cell lung cancer beginning in flat cells lining airways
- **Normal** - Healthy lung tissue

## 🚀 Features

- **Modern Web Interface** - Clean HTML/CSS/JavaScript frontend with medical-grade design
- **Real-time Analysis** - Instant classification with confidence scores
- **Visual Results** - Color-coded results with probability distributions
- **Detailed Reports** - Comprehensive analysis with recommendations
- **Responsive Design** - Works on desktop, tablet, and mobile devices

## 📊 Model Performance

- **Architecture**: Custom CNN with 28 layers
- **Parameters**: 1.24M trainable parameters
- **Input**: 150x150x3 RGB histopathological images
- **Accuracy**: 100% on test dataset (15,000 images)
- **Framework**: TensorFlow 2.15.0 / Keras 3.12.0

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/AyushmanGupta21/lung-cancer-classification.git
cd lung-cancer-classification
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Flask server:
```bash
python app.py
```

4. Open your browser and navigate to:
```
http://localhost:5000
```

## 📁 Project Structure

```
lung-cancer-classification/
├── app.py                      # Flask backend server
├── best_lung_model.h5         # Trained CNN model (14.37 MB)
├── static/
│   ├── index.html             # Main web interface
│   ├── styles.css             # Custom styling
│   └── script.js              # Frontend logic
├── requirements.txt           # Python dependencies
└── README.md                  # Documentation
```

## 🧪 Usage

1. **Upload Image**: Click the upload area or drag-and-drop a histopathological image
2. **Analyze**: Click "Start AI Analysis" to process the image
3. **View Results**: See classification, confidence score, and detailed probabilities
4. **Download Report**: Generate and download comprehensive analysis report

## ⚠️ Medical Disclaimer

This system is designed for research and educational purposes only. It should NOT be used as a substitute for professional medical diagnosis. All results must be reviewed and validated by qualified healthcare professionals.

## 🔧 Technical Details

**Backend:**
- Flask 3.0.0 web framework
- TensorFlow 2.15.0 for model inference
- CORS enabled for API access
- Health check endpoint at `/api/health`

**Frontend:**
- Vanilla JavaScript (no frameworks)
- Modern CSS with gradients and animations
- Responsive design with mobile support
- Real-time image preview

**Model:**
- Format: Keras H5 (`.h5`)
- Compatibility: Keras 3.x with `safe_mode=False`
- Optimizer: Adam
- Loss: Sparse Categorical Crossentropy

## 📝 API Endpoints

### `GET /`
Returns the main web interface

### `GET /api/health`
Health check endpoint
```json
{
  "status": "healthy",
  "model": "loaded",
  "version": "1.0.0"
}
```

### `POST /api/predict`
Image classification endpoint
- **Input**: Multipart form data with image file
- **Output**: JSON with prediction results

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 👤 Author

**Ayushman Gupta**
- GitHub: [@AyushmanGupta21](https://github.com/AyushmanGupta21)

## 🙏 Acknowledgments

- Dataset: 15,000 histopathological lung cancer images
- Framework: TensorFlow/Keras
- Deployment: Flask web server

---

**Note**: Ensure you have the model file (`best_lung_model.h5`) in the project directory before running the application.