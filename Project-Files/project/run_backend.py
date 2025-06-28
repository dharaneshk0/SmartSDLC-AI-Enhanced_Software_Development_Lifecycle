import subprocess
import sys
import os

def run_backend():
    try:
        # Change to backend directory
        os.chdir('backend')
        
        # Run FastAPI with uvicorn
        subprocess.run([
            sys.executable, '-m', 'uvicorn', 
            'main:app', 
            '--host', '0.0.0.0', 
            '--port', '8000', 
            '--reload'
        ])
    except KeyboardInterrupt:
        print("\nBackend server stopped.")
    except Exception as e:
        print(f"Error running backend: {e}")

if __name__ == "__main__":
    run_backend()