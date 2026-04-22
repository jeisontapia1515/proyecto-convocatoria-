
import sys
import os

print("Executable:", sys.executable)
print("Path:", sys.path)

try:
    from app.utils import config
    print("Successfully imported app.utils.config")
except ImportError as e:
    print("Error importing app.utils.config:", e)
    import traceback
    traceback.print_exc()
