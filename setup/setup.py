#!/usr/bin/env python3
import subprocess
import sys
import os


virt_env_name = "multimessenger_env"

def install_pip(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def install_apt(package):
    command = f"apt install {package}"
    subprocess.run(['sudo', 'bash', '-c', command])
    
def create_virt_env():
    subprocess.call(["virtualenv", f"../{virt_env_name}"])

def install_requirements():
    python_bin = f"../{virt_env_name}/bin/python"
    script_file = "install_requirements.py"
    process = subprocess.Popen([python_bin, script_file])
    process.wait()  

def create_database_and_user():
    python_bin = f"../{virt_env_name}/bin/python"
    script_file = "create_database.py"
    process = subprocess.Popen([python_bin, script_file])
    process.wait()

if __name__ == "__main__":
    install_apt("sqlite3")
    install_pip("virtualenv")
    create_virt_env()
    install_requirements()
    create_database_and_user()
    
    
    

