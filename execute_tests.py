import os
import subprocess

os.chdir(os.path.dirname(os.path.abspath(__file__)))
subprocess.run(['python', '-m', 'unittest', 'discover', '-v'])
