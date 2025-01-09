import subprocess

def is2faenabled():
    # Check if SSH 2FA is enabled by examining SSH configuration file
    try:
        sshconfig = subprocess.check_output(["cat", "/etc/ssh/sshd_config"]).decode("utf-8")
        if "ChallengeResponseAuthentication yes" in sshconfig:
            return True
        else:
            return False
    except FileNotFoundError:
        print("The SSH configuration file was not found.")
        return False
    except subprocess.CalledProcessError:
        print("Error running the 'cat' command on /etc/ssh/sshd_config.")
        return False

def main():
    if not is2faenabled():
        print("2FA is not enabled.")
    else:
        print("2FA is already enabled.")

if __name__ == "__main__":
    main()
