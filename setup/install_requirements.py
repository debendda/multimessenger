import subprocess
import sys

virt_env_name = "multimessenger_env"

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def get_requirements():
    file = open("requirements.txt", "r")
    requirements = file.read().splitlines()
    file.close()
    return requirements

if __name__ == "__main__":
    requirements = get_requirements()
    for requirement in requirements:
        install(requirement)
    
    print("Finished")
    sys.exit()