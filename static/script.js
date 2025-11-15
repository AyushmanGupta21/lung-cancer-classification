// ===================================
// Global Variables
// ===================================
let uploadedFile = null;
let currentResults = null;

// ===================================
// DOM Elements
// ===================================
const uploadZone = document.getElementById('uploadZone');
const fileInput = document.getElementById('fileInput');
const imagePreview = document.getElementById('imagePreview');
const previewImg = document.getElementById('previewImg');
const clearImageBtn = document.getElementById('clearImage');
const analyzeButton = document.getElementById('analyzeButton');
const progressSection = document.getElementById('progressSection');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');
const noResults = document.getElementById('noResults');
const resultsContent = document.getElementById('resultsContent');

// ===================================
// File Upload Handlers
// ===================================

// Click to upload
uploadZone.addEventListener('click', () => {
    fileInput.click();
});

// File input change
fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        handleFileUpload(file);
    }
});

// Drag and drop
uploadZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadZone.classList.add('dragover');
});

uploadZone.addEventListener('dragleave', () => {
    uploadZone.classList.remove('dragover');
});

uploadZone.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadZone.classList.remove('dragover');
    
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
        handleFileUpload(file);
    } else {
        showError('Please upload a valid image file');
    }
});

// ===================================
// File Upload Handler
// ===================================
function handleFileUpload(file) {
    uploadedFile = file;
    
    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImg.src = e.target.result;
        
        // Get image dimensions
        const img = new Image();
        img.onload = () => {
            document.getElementById('fileName').textContent = file.name;
            document.getElementById('fileSize').textContent = formatFileSize(file.size);
            document.getElementById('fileDimensions').textContent = `${img.width} × ${img.height} px`;
        };
        img.src = e.target.result;
    };
    reader.readAsDataURL(file);
    
    // Show preview section, hide upload zone
    uploadZone.classList.add('hidden');
    imagePreview.classList.remove('hidden');
    
    // Reset results
    resetResults();
}

// ===================================
// Clear Image Handler
// ===================================
clearImageBtn.addEventListener('click', () => {
    uploadedFile = null;
    fileInput.value = '';
    previewImg.src = '';
    
    // Hide preview, show upload zone
    imagePreview.classList.add('hidden');
    uploadZone.classList.remove('hidden');
    
    // Reset results
    resetResults();
});

// ===================================
// Analyze Button Handler
// ===================================
analyzeButton.addEventListener('click', async () => {
    if (!uploadedFile) {
        showError('Please upload an image first');
        return;
    }
    
    // Disable button
    analyzeButton.disabled = true;
    analyzeButton.textContent = '⏳ Analyzing...';
    
    // Show progress
    progressSection.classList.remove('hidden');
    
    // Simulate progress steps
    await updateProgress(10, '🤖 Loading AI model...');
    await sleep(300);
    
    await updateProgress(35, '⚙️ Preprocessing image...');
    await sleep(300);
    
    await updateProgress(60, '🧠 Running AI analysis...');
    
    // Make API call
    try {
        const formData = new FormData();
        formData.append('file', uploadedFile);
        
        const response = await fetch('/api/predict', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            await updateProgress(85, '📊 Calculating probabilities...');
            await sleep(300);
            
            await updateProgress(100, '✅ Analysis complete!');
            await sleep(500);
            
            // Display results
            displayResults(data);
        } else {
            throw new Error(data.error || 'Analysis failed');
        }
        
    } catch (error) {
        console.error('Error:', error);
        showError(`Analysis failed: ${error.message}`);
    } finally {
        // Hide progress
        progressSection.classList.add('hidden');
        progressFill.style.width = '0%';
        
        // Re-enable button
        analyzeButton.disabled = false;
        analyzeButton.textContent = '🔬 Start AI Analysis';
    }
});

// ===================================
// Display Results
// ===================================
function displayResults(data) {
    currentResults = data;
    
    // Hide no results, show results content
    noResults.classList.add('hidden');
    resultsContent.classList.remove('hidden');
    
    // Update diagnosis card
    const classInfo = data.class_info;
    document.getElementById('diagnosisEmoji').textContent = classInfo.emoji;
    document.getElementById('diagnosisClass').textContent = data.predicted_class;
    document.getElementById('diagnosisDescription').textContent = classInfo.description;
    document.getElementById('confidenceValue').textContent = `${data.confidence}%`;
    
    // Set card border color
    const diagnosisCard = document.getElementById('diagnosisCard');
    diagnosisCard.style.borderLeftColor = classInfo.color;
    
    // Update confidence meter
    const confidenceFill = document.getElementById('confidenceFill');
    setTimeout(() => {
        confidenceFill.style.width = `${data.confidence}%`;
    }, 100);
    
    // Set confidence color based on value
    if (data.confidence >= 90) {
        confidenceFill.style.background = 'linear-gradient(90deg, #51CF66 0%, #40b354 100%)';
        document.getElementById('confidenceLabel').textContent = 'Very High';
    } else if (data.confidence >= 75) {
        confidenceFill.style.background = 'linear-gradient(90deg, #FFD43B 0%, #f0c040 100%)';
        document.getElementById('confidenceLabel').textContent = 'High';
    } else if (data.confidence >= 60) {
        confidenceFill.style.background = 'linear-gradient(90deg, #FF922B 0%, #e87d20 100%)';
        document.getElementById('confidenceLabel').textContent = 'Moderate';
    } else {
        confidenceFill.style.background = 'linear-gradient(90deg, #FF6B6B 0%, #e85555 100%)';
        document.getElementById('confidenceLabel').textContent = 'Low';
    }
    
    // Update probability bars
    const probabilityBars = document.getElementById('probabilityBars');
    probabilityBars.innerHTML = '';
    
    // Sort probabilities by value (descending)
    const sortedProbs = Object.entries(data.probabilities).sort((a, b) => b[1] - a[1]);
    
    sortedProbs.forEach(([className, probability]) => {
        const isPredicted = className === data.predicted_class;
        
        const barItem = document.createElement('div');
        barItem.className = 'probability-bar-item';
        barItem.innerHTML = `
            <div class="probability-header">
                <span class="probability-name ${isPredicted ? 'predicted' : ''}">
                    ${getClassEmoji(className)} ${className} ${isPredicted ? '👈' : ''}
                </span>
                <span class="probability-value">${probability}%</span>
            </div>
            <div class="probability-bar-container">
                <div class="probability-bar-fill" style="width: 0%;"></div>
            </div>
        `;
        
        probabilityBars.appendChild(barItem);
        
        // Animate bar
        setTimeout(() => {
            barItem.querySelector('.probability-bar-fill').style.width = `${probability}%`;
        }, 100);
    });
    
    // Update action box
    document.getElementById('actionBox').textContent = classInfo.action;
    
    // Update metadata
    const now = new Date();
    document.getElementById('analysisTime').textContent = now.toLocaleTimeString();
    document.getElementById('processingTime').textContent = `${data.prediction_time}s`;
    
    // Scroll to results
    resultsContent.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// ===================================
// Download Report Handler
// ===================================
document.getElementById('downloadReport').addEventListener('click', () => {
    if (!currentResults) return;
    
    const now = new Date();
    const timestamp = now.toISOString().replace(/[:.]/g, '-');
    
    let report = `
============================================================
LUNG CANCER AI DIAGNOSIS REPORT
============================================================

Analysis Date: ${now.toLocaleDateString()}
Analysis Time: ${now.toLocaleTimeString()}

============================================================
DIAGNOSIS
============================================================

Predicted Class: ${currentResults.predicted_class}
Confidence Level: ${currentResults.confidence}%

Description:
${currentResults.class_info.description}

============================================================
PROBABILITY DISTRIBUTION
============================================================
`;
    
    Object.entries(currentResults.probabilities).forEach(([className, prob]) => {
        report += `\n${className}: ${prob}%`;
    });
    
    report += `

============================================================
RECOMMENDED ACTION
============================================================

${currentResults.class_info.action}

============================================================
IMAGE INFORMATION
============================================================

Original Dimensions: ${currentResults.image_info.original_width} × ${currentResults.image_info.original_height} px
Format: ${currentResults.image_info.format}
Processing Time: ${currentResults.prediction_time}s

============================================================
IMPORTANT MEDICAL DISCLAIMER
============================================================

This AI system is designed to ASSIST medical professionals, 
not replace them.

- Final diagnosis must be made by qualified pathologists
- Consider patient history and additional tests
- Use as a second opinion tool only
- Not approved for sole diagnostic use

============================================================
SYSTEM INFORMATION
============================================================

Model: CNN-v1.0
Framework: TensorFlow + Keras
Parameters: 1.24M
Test Accuracy: 100%

Generated by: Lung Cancer AI Diagnosis System
Report ID: ${timestamp}

============================================================
`;
    
    // Create download
    const blob = new Blob([report], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `lung_cancer_report_${timestamp}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
});

// ===================================
// Tab Switching
// ===================================
const tabs = document.querySelectorAll('.tab');
const tabPanels = document.querySelectorAll('.tab-panel');

tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        const targetTab = tab.dataset.tab;
        
        // Remove active class from all tabs and panels
        tabs.forEach(t => t.classList.remove('active'));
        tabPanels.forEach(p => p.classList.remove('active'));
        
        // Add active class to clicked tab and corresponding panel
        tab.classList.add('active');
        document.getElementById(`${targetTab}Tab`).classList.add('active');
    });
});

// ===================================
// Utility Functions
// ===================================

function resetResults() {
    currentResults = null;
    noResults.classList.remove('hidden');
    resultsContent.classList.add('hidden');
}

function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
}

function getClassEmoji(className) {
    const emojiMap = {
        'Adenocarcinoma': '🔴',
        'Squamous Cell Carcinoma': '🟠',
        'Normal': '🟢'
    };
    return emojiMap[className] || '⚪';
}

async function updateProgress(percent, text) {
    progressFill.style.width = `${percent}%`;
    progressText.textContent = text;
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function showError(message) {
    alert(`❌ Error: ${message}`);
}

// ===================================
// Check Server Health on Load
// ===================================
window.addEventListener('load', async () => {
    try {
        const response = await fetch('/api/health');
        const data = await response.json();
        
        if (data.status === 'healthy' && data.model_loaded) {
            document.getElementById('systemStatus').textContent = 'System Ready ✓';
        } else {
            document.getElementById('systemStatus').textContent = 'Model Loading...';
        }
    } catch (error) {
        console.error('Health check failed:', error);
        document.getElementById('systemStatus').textContent = 'System Error';
    }
});
