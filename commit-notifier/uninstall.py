import subprocess
from pathlib import Path
def run(cmd) :
    print(f"running command: {cmd}")
    subprocess.run(cmd, check=True)

def remove_cronjob() :
    print("Removing cron job for notifier...")
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    existing_cron = result.stdout
    lines = existing_cron.splitlines()
    new_lines = [line for line in lines if "notifier" not in line]
    new_cron = "\n".join(new_lines) + "\n"
    with open("/tmp/new_cron.txt", "w") as f :
        f.write(new_cron)
    run(["crontab", "/tmp/new_cron.txt"])
    subprocess.run(["rm", "/tmp/new_cron.txt"], check=True)
    
def remove_binary():
    target_path = Path("/usr/local/bin/notifier")
    if target_path.exists() :
        print(f"Removing binary at: {target_path}")
        run(["sudo", "rm", str(target_path)])
    else :
        print("Binary not found, skipping removal.")
        
if __name__ == "__main__":
    remove_cronjob()
    remove_binary()