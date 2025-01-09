import subprocess

def parse_find_output(output):
    suid_files = []
    lines = output.split('\n')
    for line in lines:
        parts = line.split()
        if len(parts) >= 3:
            suid_files.append((parts[0], parts[-1]))
    return suid_files

def run_find_command():
    try:
        result = subprocess.run(['find', '/', '-perm', '-u=s'], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        return None

if __name__ == "_main_":
    find_output = run_find_command()
    if find_output:
        suid_files = parse_find_output(find_output)
        if suid_files:
            print("Files with setuid bit set:")
            for file_path, permissions in suid_files:
                print(f"{file_path} - Permissions: {permissions}")
        else:
            print("No files with setuid bit set found.")
    else:
        print("Error executing find command.")
