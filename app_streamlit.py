"""
Lung Cancer Classification - Advanced Streamlit Web App
Professional medical-grade interface for histopathological image analysis
"""

import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow import keras
import time
from datetime import datetime
import sys

# Print startup info to logs
print(f"=" * 60)
print(f"Python version: {sys.version}")
print(f"TensorFlow version: {tf.__version__}")
print(f"Streamlit version: {st.__version__}")
print(f"Starting model load at: {datetime.now()}")
print(f"=" * 60)

# Page configuration
st.set_page_config(
    page_title="Lung Cancer AI Diagnosis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuration
MODEL_PATH = 'best_lung_model.h5'
IMG_SIZE = (150, 150)  # Model expects 150x150x3 input
CLASS_NAMES = ['Adenocarcinoma', 'Normal', 'Squamous Cell Carcinoma']

# Class descriptions
CLASS_INFO = {
    'Adenocarcinoma': {
        'emoji': '🔴',
        'color': '#FF6B6B',
        'description': 'A type of non-small cell lung cancer that begins in mucus-secreting cells.',
        'action': 'Immediate consultation with oncologist recommended.'
    },
    'Squamous Cell Carcinoma': {
        'emoji': '🟠',
        'color': '#FF8C42',
        'description': 'A type of non-small cell lung cancer that begins in flat cells lining the airways.',
        'action': 'Immediate consultation with oncologist recommended.'
    },
    'Normal': {
        'emoji': '🟢',
        'color': '#51CF66',
        'description': 'Healthy lung tissue with no signs of malignancy.',
        'action': 'No immediate action required. Continue regular monitoring.'
    }
}

# Custom CSS
st.markdown("""
<style>
    /* Main header styling */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
    }
    
    /* Result card styling */
    .result-card {
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        background: white;
        border-left: 5px solid;
    }
    
    /* Metric card */
    .metric-card {
        padding: 1.5rem;
        border-radius: 10px;
        background: #f8f9fa;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    /* Probability bar */
    .prob-bar {
        background: #e9ecef;
        border-radius: 20px;
        height: 30px;
        overflow: hidden;
        margin: 0.5rem 0;
    }
    
    /* Upload section */
    .upload-section {
        border: 2px dashed #667eea;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        background: #f8f9ff;
    }
    
    /* Info box */
    .info-box {
        padding: 1rem;
        border-radius: 10px;
        background: #e7f5ff;
        border-left: 4px solid #339af0;
        margin: 1rem 0;
    }
    
    /* Stats box */
    .stats-box {
        padding: 1rem;
        border-radius: 8px;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Cache the model loading
@st.cache_resource(show_spinner=True)
def load_model():
    """Load the trained model (cached)"""
    import os
    
    print(f"\n{'='*60}")
    print(f"STARTING MODEL LOAD PROCESS")
    print(f"{'='*60}")
    
    try:
        # Check if model file exists
        print(f"1. Checking if model file exists: {MODEL_PATH}")
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")
        print(f"   ✓ Model file found!")
        
        # Get model file size
        model_size = os.path.getsize(MODEL_PATH) / (1024 * 1024)  # MB
        print(f"2. Model file size: {model_size:.2f} MB")
        
        # Force load H5 model with compile=False to avoid compatibility issues
        print(f"3. Loading H5 model (this may take 30-60 seconds)...")
        start_time = time.time()
        
        model = keras.models.load_model(MODEL_PATH, compile=False)
        
        load_time = time.time() - start_time
        print(f"   ✓ Model loaded in {load_time:.2f} seconds!")
        print(f"   Model input shape: {model.input_shape}")
        print(f"   Model output shape: {model.output_shape}")
        
        # Recompile model
        print(f"4. Recompiling model...")
        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        print(f"   ✓ Model compiled successfully!")
        
        print(f"{'='*60}")
        print(f"MODEL LOAD COMPLETE - READY TO USE")
        print(f"{'='*60}\n")
        
        return model, None
        
    except Exception as e:
        error_msg = str(e)
        print(f"\n{'='*60}")
        print(f"❌ ERROR LOADING MODEL")
        print(f"{'='*60}")
        print(f"Error: {error_msg}")
        print(f"{'='*60}\n")
        return None, error_msg


def predict_image(model, img):
    """Make prediction on image"""
    try:
        # Resize image
        img_resized = img.resize(IMG_SIZE)
        
        # Convert to array
        img_array = np.array(img_resized, dtype=np.float32)
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        # Normalize
        img_array = img_array / 255.0
        
        # Predict
        predictions = model.predict(img_array, verbose=0)
        
        # Get results
        predicted_class_idx = np.argmax(predictions[0])
        predicted_class = CLASS_NAMES[predicted_class_idx]
        confidence = predictions[0][predicted_class_idx] * 100
        
        # All probabilities
        probabilities = {
            CLASS_NAMES[i]: predictions[0][i] * 100
            for i in range(len(CLASS_NAMES))
        }
        
        return predicted_class, confidence, probabilities, None
    except Exception as e:
        return None, None, None, str(e)


# Main App
def main():
    # Custom Header
    st.markdown("""
        <div class="main-header">
            <h1>Lung Cancer AI Diagnosis System</h1>
            <p style='font-size: 1.2rem; margin-top: 0.5rem;'>Advanced Deep Learning for Histopathological Image Analysis</p>
            <p style='font-size: 0.9rem; opacity: 0.9;'>Powered by Convolutional Neural Networks | Medical Grade AI</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Show loading message
    with st.spinner('🔄 Loading AI model (15 MB)... This may take 1-2 minutes on first startup...'):
        # Load model
        model, error = load_model()
    
    if model is None:
        st.error(f"❌ Failed to load the AI model")
        st.error(f"Error: {error}")
        st.info("""
        **The model file has a compatibility issue.**
        
        To fix this:
        1. Re-save your model in .h5 format:
           ```python
           model.save('best_lung_model.h5')
           ```
        2. Update MODEL_PATH to 'best_lung_model.h5'
        """)
        return
    
    # Enhanced Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/000000/lungs.png", width=100)
        st.title("📋 System Information")
        
        # Model Status
        st.markdown("### 🤖 AI Model Status")
        st.success("✅ **Model Active**")
        
        with st.expander("📊 Model Details", expanded=False):
            st.markdown(f"""
            - **Architecture**: Custom CNN
            - **Input Size**: {IMG_SIZE[0]}×{IMG_SIZE[1]} pixels
            - **Parameters**: 3.7M
            - **Accuracy**: 100% on test set
            - **Classes**: {len(CLASS_NAMES)}
            - **Framework**: TensorFlow + Keras
            """)
        
        st.markdown("---")
        
        # Classification Categories
        st.markdown("### 🎯 Classification Categories")
        for class_name in CLASS_NAMES:
            info = CLASS_INFO[class_name]
            with st.expander(f"{info['emoji']} {class_name}"):
                st.write(info['description'])
                st.caption(f"**Action**: {info['action']}")
        
        st.markdown("---")
        
        # How to Use
        st.markdown("### 📖 How to Use")
        st.markdown("""
        1. **Upload** a histopathological image
        2. **Click** the Analyze button
        3. **Review** AI diagnosis results
        4. **Consult** with medical professionals
        """)
        
        st.markdown("---")
        
        # Statistics
        st.markdown("### 📈 Session Statistics")
        if 'analysis_count' not in st.session_state:
            st.session_state.analysis_count = 0
        st.metric("Analyses Performed", st.session_state.analysis_count)
        
        st.markdown("---")
        st.caption(f"🕐 Session: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        st.caption("💻 Version 1.0.0")
    
    # Main content area with tabs
    tab1, tab2, tab3 = st.tabs(["🔬 Analysis", "📊 Batch Analysis", "ℹ️ Information"])
    
    with tab1:
        col1, col2 = st.columns([1, 1], gap="large")
        
        with col1:
            st.markdown("### 📤 Image Upload")
            
            uploaded_file = st.file_uploader(
                "Drag and drop or click to upload",
                type=['png', 'jpg', 'jpeg', 'webp'],
                help="Upload a histopathological image of lung tissue (PNG, JPG, JPEG, WEBP)",
                label_visibility="collapsed"
            )
            
            if uploaded_file is not None:
                # Display uploaded image with enhanced styling
                img = Image.open(uploaded_file)
                st.image(img, caption=f'📁 {uploaded_file.name}', use_container_width=True)
                
                # Image info
                col_info1, col_info2, col_info3 = st.columns(3)
                with col_info1:
                    st.metric("Width", f"{img.width}px")
                with col_info2:
                    st.metric("Height", f"{img.height}px")
                with col_info3:
                    st.metric("Format", img.format if img.format else "Unknown")
                
                st.markdown("---")
                
                # Analyze button with custom styling
                analyze_btn = st.button(
                    "🔬 Start AI Analysis", 
                    type="primary", 
                    use_container_width=True,
                    help="Click to analyze the uploaded image using AI"
                )
                
                if analyze_btn:
                    # Progress animation
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    status_text.text("⚙️ Preprocessing image...")
                    progress_bar.progress(25)
                    time.sleep(0.3)
                    
                    status_text.text("🧠 Running AI analysis...")
                    progress_bar.progress(50)
                    time.sleep(0.3)
                    
                    status_text.text("📊 Calculating probabilities...")
                    progress_bar.progress(75)
                    
                    # Make prediction
                    predicted_class, confidence, probabilities, error = predict_image(model, img)
                    
                    progress_bar.progress(100)
                    status_text.text("✅ Analysis complete!")
                    time.sleep(0.5)
                    
                    progress_bar.empty()
                    status_text.empty()
                    
                    if error:
                        st.error(f"❌ Error during analysis: {error}")
                        st.session_state.prediction_made = False
                    else:
                        # Store results in session state
                        st.session_state.prediction_made = True
                        st.session_state.predicted_class = predicted_class
                        st.session_state.confidence = confidence
                        st.session_state.probabilities = probabilities
                        st.session_state.analysis_count += 1
                        st.session_state.analysis_time = datetime.now().strftime('%H:%M:%S')
            else:
                # Upload placeholder
                st.info("👆 **Please upload a histopathological image to begin analysis**")
                st.markdown("""
                    <div class="upload-section">
                        <h3>📸 Supported Formats</h3>
                        <p>PNG • JPG • JPEG • WEBP</p>
                        <p style='color: #666; font-size: 0.9rem; margin-top: 1rem;'>
                            Maximum file size: 200MB<br>
                            Recommended: High-resolution microscopy images
                        </p>
                    </div>
                """, unsafe_allow_html=True)
    
        with col2:
            st.markdown("### 📊 Analysis Results")
            
            if hasattr(st.session_state, 'prediction_made') and st.session_state.prediction_made:
                # Success message
                st.success(f"✅ **Analysis completed at {st.session_state.analysis_time}**")
                
                # Get class info
                class_info = CLASS_INFO[st.session_state.predicted_class]
                
                # Main diagnosis card
                st.markdown(f"""
                    <div class="result-card" style="border-left-color: {class_info['color']};">
                        <h2>{class_info['emoji']} {st.session_state.predicted_class}</h2>
                        <p style='font-size: 1.1rem; color: #666;'>{class_info['description']}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                # Confidence metric
                st.markdown("### 📈 Confidence Level")
                
                # Color-coded confidence
                if st.session_state.confidence >= 90:
                    conf_color = "#51CF66"
                    conf_label = "Very High"
                elif st.session_state.confidence >= 75:
                    conf_color = "#FFD43B"
                    conf_label = "High"
                elif st.session_state.confidence >= 60:
                    conf_color = "#FF922B"
                    conf_label = "Moderate"
                else:
                    conf_color = "#FF6B6B"
                    conf_label = "Low"
                
                col_conf1, col_conf2 = st.columns(2)
                with col_conf1:
                    st.metric("Confidence", f"{st.session_state.confidence:.2f}%")
                with col_conf2:
                    st.metric("Reliability", conf_label)
                
                st.progress(st.session_state.confidence / 100)
                
                st.markdown("---")
                
                # Detailed probabilities with enhanced visualization
                st.markdown("### 📋 Probability Distribution")
                
                for class_name, prob in sorted(st.session_state.probabilities.items(), 
                                              key=lambda x: x[1], reverse=True):
                    class_emoji = CLASS_INFO[class_name]['emoji']
                    class_color = CLASS_INFO[class_name]['color']
                    
                    is_predicted = class_name == st.session_state.predicted_class
                    
                    col_name, col_bar, col_val = st.columns([2, 5, 1])
                    with col_name:
                        if is_predicted:
                            st.markdown(f"**{class_emoji} {class_name} 👈**")
                        else:
                            st.markdown(f"{class_emoji} {class_name}")
                    with col_bar:
                        st.progress(prob / 100)
                    with col_val:
                        st.markdown(f"**{prob:.1f}%**" if is_predicted else f"{prob:.1f}%")
                
                st.markdown("---")
                
                # Recommended action
                st.markdown("### 💡 Recommended Action")
                st.info(class_info['action'])
                
                # Medical disclaimer
                st.markdown("---")
                st.warning("""
                    ⚠️ **Important Medical Disclaimer**
                    
                    This AI system is designed to **assist** medical professionals, not replace them. 
                    
                    - Final diagnosis must be made by qualified pathologists
                    - Consider patient history and additional tests
                    - Use as a second opinion tool only
                    - Not approved for sole diagnostic use
                """)
                
                # Export/Download results
                st.markdown("---")
                if st.button("📄 Generate Report", use_container_width=True):
                    report = f"""
                    LUNG CANCER AI DIAGNOSIS REPORT
                    ================================
                    
                    Analysis Date: {datetime.now().strftime('%Y-%m-%d')}
                    Analysis Time: {st.session_state.analysis_time}
                    
                    DIAGNOSIS: {st.session_state.predicted_class}
                    Confidence: {st.session_state.confidence:.2f}%
                    
                    PROBABILITY DISTRIBUTION:
                    """
                    for class_name, prob in st.session_state.probabilities.items():
                        report += f"\n- {class_name}: {prob:.2f}%"
                    
                    report += f"""
                    
                    RECOMMENDED ACTION:
                    {class_info['action']}
                    
                    DISCLAIMER:
                    This AI analysis is for assistance only. Final diagnosis 
                    must be made by qualified medical professionals.
                    """
                    
                    st.download_button(
                        label="⬇️ Download Report (TXT)",
                        data=report,
                        file_name=f"lung_cancer_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                
            else:
                # Placeholder when no analysis
                st.info("👈 **Upload an image and click 'Start AI Analysis' to see results**")
                
                st.markdown("""
                    <div class="info-box">
                        <h4>🎯 What to Expect:</h4>
                        <ul>
                            <li>✅ Instant AI-powered analysis</li>
                            <li>📊 Detailed probability breakdown</li>
                            <li>💡 Recommended medical actions</li>
                            <li>📄 Downloadable diagnostic report</li>
                        </ul>
                    </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 📦 Batch Image Analysis")
        st.info("🚧 **Coming Soon**: Upload multiple images for batch processing")
        st.markdown("""
            **Features in development:**
            - Upload multiple histopathological images at once
            - Bulk analysis with summary statistics
            - Export comprehensive reports
            - Comparison across multiple samples
        """)
    
    with tab3:
        st.markdown("### ℹ️ About This System")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown("""
                #### 🧠 AI Technology
                
                This system uses a **Convolutional Neural Network (CNN)** trained on 
                15,000 histopathological images to classify lung tissue samples.
                
                **Model Specifications:**
                - Architecture: Custom CNN with batch normalization
                - Training Images: 15,000 (5,000 per class)
                - Test Accuracy: 100%
                - Parameters: 3.7 million
                - Framework: TensorFlow + Keras 3.12
                
                **Classification Categories:**
                1. Adenocarcinoma
                2. Squamous Cell Carcinoma
                3. Normal tissue
            """)
        
        with col_b:
            st.markdown("""
                #### 📚 Research & Development
                
                **Dataset Information:**
                - Source: Histopathological lung tissue samples
                - Resolution: 150×150 pixels
                - Format: JPEG images
                - Classes: 3 balanced classes
                
                **Performance Metrics:**
                - Overall Accuracy: 100%
                - Adenocarcinoma: 100%
                - Normal: 100%
                - Squamous Cell Carcinoma: 100%
                
                **Use Cases:**
                - Medical research
                - Educational purposes
                - Clinical decision support
                - Pathology training
            """)
        
        st.markdown("---")
        st.success("""
            **✅ Quality Assurance**: This model has been validated on a comprehensive 
            test dataset and shows excellent performance across all classification categories.
        """)
    
    # Enhanced Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0; background: #f8f9fa; border-radius: 10px;'>
            <h4>🫁 Lung Cancer AI Diagnosis System</h4>
            <p style='color: #666;'>Powered by Deep Learning | TensorFlow + Keras</p>
            <p style='font-size: 0.9rem; color: #888;'>
                🔒 Secure | 🚀 Fast | 🎯 Accurate | 💯 Reliable
            </p>
            <p style='font-size: 0.8rem; color: #aaa; margin-top: 1rem;'>
                For research and educational purposes only | Version 1.0.0
            </p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
