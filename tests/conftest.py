import sys
from pathlib import Path 

PATH = Path(__file__).parent.parent
print(PATH)
sys.path.append(str(PATH))