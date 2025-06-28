import subprocess
import sys
import os

def run_frontend():
    try:
        # Change to frontend directory
        os.chdir('frontend')
        
        # Run Streamlit
        subprocess.run([
            sys.executable, '-m', 'streamlit', 
            'run', 'Home.py',
            '--server.port', '8501',
            '--server.address', '0.0.0.0'
        ])
    except KeyboardInterrupt:
        print("\nFrontend server stopped.")
    except Exception as e:
        print(f"Error running frontend: {e}")

if __name__ == "__main__":
    run_frontend()