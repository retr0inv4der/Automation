import os
import sys
import subprocess
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.resolve()
VENV_DIR = PROJECT_DIR / "venv"


def run(cmd) :
    print(f"running command: {cmd}")
    subprocess.run(cmd, check=True)

def create_venv() :
    print(f"Creating virtual environment at: {VENV_DIR}")
    run([sys.executable, "-m", "venv", VENV_DIR])


def install_dependencies() :
    pip_executable = VENV_DIR / "bin" / "pip"
    print(f"Installing dependencies using: {pip_executable}")
    run([str(pip_executable), "install", "-r", str(PROJECT_DIR / "requirements.txt")])


def compile_resources() :
    print("compiling resources...")
    pyinstaller_executable = VENV_DIR / "bin" / "pyinstaller"
    spec_file = PROJECT_DIR / "notifier.py"
    run([str(pyinstaller_executable), "--onefile", str(spec_file)])
    #copy the compiled binary to /usr/local/bin
    dist_dir = PROJECT_DIR / "dist"
    target_path = Path("/usr/local/bin/notifier")
    print(f"copying compiled binary to: {target_path}")
    run(["sudo","cp", str(dist_dir / "notifier"), str(target_path)])
    #sudo chmod +x /usr/local/bin/notifier
    run(["sudo","chmod", "+x", str(target_path)])
    
    print("cleaning up build artifacts...")
    
    #remove build directory
    build_dir = PROJECT_DIR / "build"
    if build_dir.exists() and build_dir.is_dir() :
        print(f"removing build directory: {build_dir}")
        subprocess.run(["rm", "-rf", str(build_dir)], check=True)
    
    #remove dist directory
    dist_dir_parent = PROJECT_DIR / "dist"
    if dist_dir_parent.exists() and dist_dir_parent.is_dir() :
        print(f"Removing dist directory: {dist_dir_parent}")
        subprocess.run(["rm", "-rf", str(dist_dir_parent)], check=True)

    #remove the notifier.spec file
    spec_file_path = PROJECT_DIR / "notifier.spec"
    if spec_file_path.exists() :
        print(f"Removing spec file: {spec_file_path}")
        subprocess.run(["rm", str(spec_file_path)], check=True)
        
    #remove the venv directory
    if VENV_DIR.exists() and VENV_DIR.is_dir() :
        print(f"Removing virtual environment directory: {VENV_DIR}")
        subprocess.run(["rm", "-rf", str(VENV_DIR)], check=True)
        

def create_cronjob(user , repo):
    cron_line = f"*/1 * * * * /usr/local/bin/notifier {user} {repo} >> /var/log/notifier.log 2>&1 \n"
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    existing_cron = result.stdout
    if cron_line.strip() in existing_cron :
        print("Cron job already exists. Skipping addition.")
        return
    new_cron = existing_cron + cron_line
    subprocess.run(["crontab", "-"], input=new_cron, text=True)
    
    
def main() :
    if sys.argv.__len__() != 3 :
        print("Usage: python install.py <github-username> <repository-name>")
        sys.exit(1)
    create_venv()
    install_dependencies()
    compile_resources()
    print("installation and compilation complete.")
    create_cronjob(sys.argv[1] , sys.argv[2])
    print("cron job created/verified.")
    
if __name__ == "__main__" :
    main()