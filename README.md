---
title: Lung Cancer AI Diagnosis
emoji: 🫁
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
---

# 🫁 Lung Cancer AI Diagnosis System

Advanced Deep Learning system for histopathological lung cancer image analysis using Convolutional Neural Networks.

## 🎯 Features

- **AI-Powered Classification**: Analyzes histopathological lung tissue images
- **3 Classification Categories**:
  - 🔴 Adenocarcinoma
  - 🟠 Squamous Cell Carcinoma  
  - 🟢 Normal Tissue
- **Professional Medical Interface**: Clean, intuitive UI designed for medical professionals
- **Detailed Analysis**: Confidence scores and probability distributions
- **Report Generation**: Downloadable diagnostic reports
- **Real-time Processing**: Instant AI predictions

## 🧠 Model Specifications

- **Architecture**: Custom Convolutional Neural Network (CNN)
- **Training Dataset**: 15,000 histopathological images (5,000 per class)
- **Test Accuracy**: 100%
- **Parameters**: 3.7 million
- **Input Size**: 150×150 pixels
- **Framework**: TensorFlow 2.15 + Keras

## 🚀 How to Use

1. **Upload Image**: Click to upload a histopathological lung tissue image (PNG, JPG, JPEG, WEBP)
2. **Analyze**: Click "Start AI Analysis" button
3. **Review Results**: View predicted diagnosis with confidence level
4. **Generate Report**: Download detailed diagnostic report

## 📊 Performance Metrics

- Overall Accuracy: **100%**
- Adenocarcinoma Detection: **100%**
- Squamous Cell Carcinoma Detection: **100%**
- Normal Tissue Detection: **100%**

## 💻 Local Installation

```bash
# Clone the repository
git clone https://github.com/AyushmanGupta21/lung-cancer-classification
cd lung-cancer-classification

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app_streamlit.py
```

## ⚠️ Medical Disclaimer

This AI system is designed to **assist** medical professionals, not replace them.

- Final diagnosis must be made by qualified pathologists
- Consider patient history and additional clinical tests
- Use as a second opinion tool only
- Not approved for sole diagnostic use

## �️ Technical Stack

- **Framework**: TensorFlow 2.15.0 + Keras 3.12.0
- **Frontend**: Streamlit
- **Image Processing**: PIL, NumPy
- **Model Format**: Keras (.keras)

## 📝 License

For research and educational purposes only.
