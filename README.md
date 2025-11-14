# 🏥 Lung Cancer Classification System

AI-powered web application for classifying lung histopathological images into three categories:
- **Adenocarcinoma** (Lung cancer type 1)
- **Normal** (Healthy lung tissue)
- **Squamous Cell Carcinoma** (Lung cancer type 2)

## 🎯 Features

- ✅ **High Accuracy**: 100% accuracy on test dataset
- 🖼️ **Easy Upload**: Drag-and-drop interface for doctors
- ⚡ **Real-time Analysis**: Instant classification results
- 📊 **Confidence Scores**: Detailed probability breakdown
- 🎨 **Professional UI**: Clean, medical-grade interface

## 🚀 Model Performance

- **Architecture**: Custom CNN with batch normalization and dropout
- **Input Size**: 150x150x3 (RGB images)
- **Total Parameters**: 3.7M (14.21 MB)
- **Trainable Parameters**: 1.2M (4.73 MB)
- **Test Accuracy**: 100%

## 💻 Local Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd lung_cancer

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app_streamlit.py
```

## 📊 Dataset

- **Total Images**: 15,000 histopathological images
- **Classes**: 3 (5,000 images per class)
- **Image Format**: JPEG
- **Resolution**: 150x150 pixels

## ⚠️ Medical Disclaimer

This tool is for educational and research purposes only. It should not be used as the sole basis for medical diagnosis. Always consult with qualified healthcare professionals for accurate medical diagnosis and treatment.

## 🔧 Technical Stack

- **Framework**: TensorFlow 2.15.0 + Keras 3.12.0
- **Frontend**: Streamlit
- **Image Processing**: PIL, NumPy
- **Model Format**: Keras (.keras)

## 📝 License

For research and educational purposes only.
