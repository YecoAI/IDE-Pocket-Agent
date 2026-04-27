import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
 from src.main import main
 try:
 main()
 except KeyboardInterrupt:
 pass
