import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.app import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8111, debug=True)
