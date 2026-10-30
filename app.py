# Fallback root app loader pointing to app/main.py
import sys
import os

# Add root directory to path
root_dir = os.path.dirname(os.path.abspath(__file__))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# Execute main app module
from app.main import *
