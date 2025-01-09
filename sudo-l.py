import subprocess

def run_sudo_l():
    try:
        result = subprocess.run(['sudo', 'find','/', '-perm', '-u=s'], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        return None

if __name__ == "_main_":
    sudo_l_output = run_sudo_l()
    if sudo_l_output:
        print("Output of sudo -l command:")
        print(sudo_l_output)
    else:
        print("Error executing command with sudo.")
