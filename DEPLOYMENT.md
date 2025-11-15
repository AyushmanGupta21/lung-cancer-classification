# PythonAnywhere Deployment Guide

## Free Deployment Instructions

### 1. Sign Up
- Go to: https://www.pythonanywhere.com/registration/register/beginner/
- Create a free account

### 2. Open Bash Console
- Click "Consoles" tab
- Click "Bash"

### 3. Clone Your Repository
```bash
git clone https://github.com/AyushmanGupta21/lung-cancer-classification.git
cd lung-cancer-classification
```

### 4. Install Dependencies
```bash
pip3 install --user -r requirements.txt
```

### 5. Create Web App
- Go to "Web" tab
- Click "Add a new web app"
- Choose "Manual configuration"
- Choose "Python 3.10"

### 6. Configure WSGI File
- In "Code" section, click on WSGI configuration file
- Replace contents with:
```python
import sys
import os

# Add your project directory
project_home = '/home/YOUR_USERNAME/lung-cancer-classification'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

from app import app as application
```
- Replace `YOUR_USERNAME` with your PythonAnywhere username

### 7. Set Static Files
In "Static files" section, add:
- URL: `/styles.css` → Directory: `/home/YOUR_USERNAME/lung-cancer-classification/static/styles.css`
- URL: `/script.js` → Directory: `/home/YOUR_USERNAME/lung-cancer-classification/static/script.js`
- URL: `/static/` → Directory: `/home/YOUR_USERNAME/lung-cancer-classification/static/`

### 8. Reload
- Click green "Reload" button
- Visit your app at: `https://YOUR_USERNAME.pythonanywhere.com`

## Notes
- Free tier has CPU limits (100 seconds/day)
- Your model is 14MB, should work fine
- App stays online 24/7 (no spin-down)

## Alternative Free Options

If PythonAnywhere doesn't work:

### Render.com (with spin-down)
- Always free
- Spins down after 15 min inactivity
- 30-60 sec wake-up time
- Good for demos

### Railway (with $5 credit)
- $5/month free credit
- Always on
- Faster performance
- Credit usually enough for small apps
