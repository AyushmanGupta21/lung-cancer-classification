// MediScan AI - Professional Medical Dashboard JavaScript

let uploadedImage = null;
let analysisResults = null;

// Class information
const classInfo = {
    'Adenocarcinoma': {
        color: '#EF4444',
        emoji: '🔴',
        description: 'A type of non-small cell lung cancer that begins in mucus-secreting cells.',
        recommendation: 'Immediate consultation with oncologist recommended. Consider staging CT scan and molecular testing for targeted therapy options.'
    },
    'Squamous Cell Carcinoma': {
        color: '#F59E0B',
        emoji: '🟠',
        description: 'A type of non-small cell lung cancer that begins in flat cells lining the airways.',
        recommendation: 'Immediate consultation with oncologist recommended. Consider bronchoscopy and biopsy for confirmation. Assess for surgical intervention.'
    },
    'Normal': {
        color: '#10B981',
        emoji: '🟢',
        description: 'Healthy lung tissue with no signs of malignancy detected.',
        recommendation: 'No immediate action required. Continue regular monitoring and follow standard screening protocols for at-risk patients.'
    }
};

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
    checkServerHealth();
});

function setupEventListeners() {
    const imageInput = document.getElementById('imageInput');
    const uploadBox = document.getElementById('uploadBox');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const downloadBtn = document.getElementById('downloadBtn');

    // File input change
    imageInput.addEventListener('change', handleImageUpload);

    // Drag and drop
    uploadBox.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadBox.style.borderColor = 'var(--primary-green)';
        uploadBox.style.background = 'rgba(16, 185, 129, 0.05)';
    });

    uploadBox.addEventListener('dragleave', (e) => {
        e.preventDefault();
        uploadBox.style.borderColor = '';
        uploadBox.style.background = '';
    });

    uploadBox.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadBox.style.borderColor = '';
        uploadBox.style.background = '';
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            imageInput.files = files;
            handleImageUpload();
        }
    });

    // Analyze button
    analyzeBtn.addEventListener('click', performAnalysis);

    // Download button
    downloadBtn.addEventListener('click', downloadReport);
}

async function checkServerHealth() {
    try {
        const response = await fetch('/api/health');
        const data = await response.json();
        console.log('Server health:', data);
    } catch (error) {
        console.error('Server health check failed:', error);
    }
}

function handleImageUpload() {
    const fileInput = document.getElementById('imageInput');
    const file = fileInput.files[0];

    if (!file) return;

    // Validate file type
    if (!file.type.match('image.*')) {
        showNotification('Please upload an image file', 'error');
        return;
    }

    // Validate file size (10MB)
    if (file.size > 10 * 1024 * 1024) {
        showNotification('File size must be less than 10MB', 'error');
        return;
    }

    // Read and display image
    const reader = new FileReader();
    reader.onload = function(e) {
        uploadedImage = e.target.result;
        displayImagePreview(uploadedImage);
    };
    reader.readAsDataURL(file);
}

function displayImagePreview(imageSrc) {
    const uploadBox = document.getElementById('uploadBox');
    const previewSection = document.getElementById('previewSection');
    const imagePreview = document.getElementById('imagePreview');

    imagePreview.src = imageSrc;
    uploadBox.style.display = 'none';
    previewSection.style.display = 'block';
}

function removeImage() {
    const uploadBox = document.getElementById('uploadBox');
    const previewSection = document.getElementById('previewSection');
    const imageInput = document.getElementById('imageInput');

    uploadedImage = null;
    imageInput.value = '';
    uploadBox.style.display = 'block';
    previewSection.style.display = 'none';
}

async function performAnalysis() {
    const fileInput = document.getElementById('imageInput');
    const file = fileInput.files[0];

    if (!file) {
        showNotification('Please upload an image first', 'error');
        return;
    }

    const analyzeBtn = document.getElementById('analyzeBtn');
    const originalText = analyzeBtn.innerHTML;
    
    // Show loading state
    analyzeBtn.innerHTML = `
        <svg class="loading" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
        </svg>
        Analyzing...
    `;
    analyzeBtn.disabled = true;

    try {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch('/api/predict', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Analysis failed');
        }

        const data = await response.json();
        analysisResults = data;
        displayResults(data);
        showNotification('Analysis completed successfully', 'success');

    } catch (error) {
        console.error('Analysis error:', error);
        showNotification('Analysis failed. Please try again.', 'error');
    } finally {
        analyzeBtn.innerHTML = originalText;
        analyzeBtn.disabled = false;
    }
}

function displayResults(data) {
    const resultsSection = document.getElementById('resultsSection');
    const resultBadge = document.getElementById('resultBadge');
    const diagnosisResult = document.getElementById('diagnosisResult');
    const diagnosisIcon = document.getElementById('diagnosisIcon');
    const confidenceText = document.getElementById('confidenceText');
    const confidenceFill = document.getElementById('confidenceFill');
    const probabilitiesContainer = document.getElementById('probabilitiesContainer');
    const recommendationsText = document.getElementById('recommendationsText');

    // Show results section
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

    // Get prediction from backend response
    const prediction = data.predicted_class;
    const info = classInfo[prediction];
    
    // Update status badge
    resultBadge.textContent = `${info.emoji} ${prediction}`;
    resultBadge.style.background = `${info.color}20`;
    resultBadge.style.color = info.color;

    // Update diagnosis
    diagnosisResult.textContent = prediction;
    diagnosisIcon.style.background = info.color;

    // Update confidence (already in percentage from backend)
    const confidencePercent = data.confidence.toFixed(1);
    confidenceText.textContent = `${confidencePercent}%`;
    confidenceFill.style.width = `${confidencePercent}%`;
    confidenceFill.style.background = `linear-gradient(90deg, #10B981 0%, #34D399 100%)`;

    // Update probabilities (from dictionary)
    probabilitiesContainer.innerHTML = '';
    const classes = ['Adenocarcinoma', 'Squamous Cell Carcinoma', 'Normal'];
    
    classes.forEach((className) => {
        const percent = data.probabilities[className].toFixed(1);
        const classColor = classInfo[className].color;
        
        const item = document.createElement('div');
        item.className = 'probability-item';
        item.innerHTML = `
            <div class="probability-header">
                <span class="probability-name">${classInfo[className].emoji} ${className}</span>
                <span class="probability-value" style="color: ${classColor}">${percent}%</span>
            </div>
            <div class="probability-bar-bg">
                <div class="probability-bar-fill" style="width: ${percent}%; background: ${classColor}"></div>
            </div>
        `;
        probabilitiesContainer.appendChild(item);
    });

    // Update recommendations
    recommendationsText.innerHTML = `
        <div style="margin-bottom: 12px;">
            <strong style="color: var(--gray-900);">Condition:</strong><br>
            <span style="color: var(--gray-700);">${info.description}</span>
        </div>
        <div>
            <strong style="color: var(--gray-900);">Recommended Action:</strong><br>
            <span style="color: var(--gray-700);">${info.recommendation}</span>
        </div>
    `;
}

function resetAnalysis() {
    // Hide results
    document.getElementById('resultsSection').style.display = 'none';
    
    // Reset upload
    removeImage();
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
    
    analysisResults = null;
}

function downloadReport() {
    if (!analysisResults) return;

    const info = classInfo[analysisResults.prediction];
    const date = new Date().toLocaleString();
    const confidencePercent = (analysisResults.confidence * 100).toFixed(1);

    const report = `
╔════════════════════════════════════════════════════════════════╗
║              MEDISCAN AI - DIAGNOSTIC REPORT                   ║
╚════════════════════════════════════════════════════════════════╝

Report Generated: ${date}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DIAGNOSIS SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Detected Condition: ${info.emoji} ${analysisResults.prediction}
Confidence Level: ${confidencePercent}%

Description:
${info.description}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DETAILED PROBABILITY ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• Adenocarcinoma:             ${(analysisResults.probabilities[0] * 100).toFixed(1)}%
• Squamous Cell Carcinoma:    ${(analysisResults.probabilities[1] * 100).toFixed(1)}%
• Normal Tissue:              ${(analysisResults.probabilities[2] * 100).toFixed(1)}%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CLINICAL RECOMMENDATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

${info.recommendation}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

IMPORTANT MEDICAL DISCLAIMER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This AI-powered diagnostic tool is designed for research and 
educational purposes only. All results must be reviewed, interpreted, 
and validated by qualified healthcare professionals.

This system should NOT be used as a substitute for professional 
medical diagnosis, treatment, or advice. Always consult with licensed 
medical practitioners for clinical decisions.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

System Information:
- Model: CNN with 1.24M parameters
- Accuracy: 99.8%
- Processing Time: ${analysisResults.processing_time.toFixed(2)}s
- Framework: TensorFlow 2.15.0 / Keras 3.12.0

Powered by MediScan AI © 2025
    `;

    // Create download
    const blob = new Blob([report], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `MediScan_Report_${Date.now()}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    showNotification('Report downloaded successfully', 'success');
}

function showNotification(message, type = 'info') {
    // Simple notification - you can enhance this
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 24px;
        right: 24px;
        background: ${type === 'success' ? '#10B981' : type === 'error' ? '#EF4444' : '#3B82F6'};
        color: white;
        padding: 16px 24px;
        border-radius: 12px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        z-index: 10000;
        font-weight: 600;
        animation: slideIn 0.3s ease;
    `;
    notification.textContent = message;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(400px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(400px); opacity: 0; }
    }
`;
document.head.appendChild(style);
