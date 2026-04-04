#!/usr/bin/env python
"""
Flask App Runner for Email Generation System
This script starts the Flask web application for generating and scheduling emails.
"""

import os
import sys
from pathlib import Path

# Add the src directory to Python path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

from email_geneartion.app import app

if __name__ == '__main__':
    print("🚀 Starting AI Email Generator Web Application...")
    print("📧 Access the application at: http://localhost:5000")
    print("⏰ Features include:")
    print("   - AI-powered email generation")
    print("   - Document upload and analysis") 
    print("   - Email scheduling")
    print("   - Automatic attachment handling")
    print("\n" + "="*50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)

