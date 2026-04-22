
import sys
import os

print("Executable:", sys.executable)
print("Path:", sys.path)

try:
    import pydantic
    print("Pydantic version:", pydantic.__version__)
except ImportError as e:
    print("Error importing pydantic:", e)

try:
    import pydantic_settings
    print("pydantic_settings version:", pydantic_settings.__version__)
except ImportError as e:
    print("Error importing pydantic_settings:", e)
    
    site_packages = [p for p in sys.path if 'site-packages' in p][0]
    try:
        files = os.listdir(site_packages)
        print(f"Is pydantic_settings in site-packages? {'pydantic_settings' in files}")
        # It might be installed as pydantic_settings (folder) or pydantic-settings (dist-info)
        # But the import package name is pydantic_settings
    except Exception as ex:
        print(f"Error listing site-packages: {ex}")
