# WSGI entry point for PythonAnywhere deployment
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/yourusername/lung_cancer'  # Update with your actual path
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Import the Flask app
from app import app as application
