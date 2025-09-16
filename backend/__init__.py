# Backend root __init__.py
from pathlib import Path
import sys

# Add the project root to PYTHONPATH
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)
