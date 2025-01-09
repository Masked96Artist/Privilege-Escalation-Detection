import os

def find_setuid_files(root_dir='/'):
    setuid_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                
                if os.stat(file_path).st_mode & 0o4000:
                    setuid_files.append(file_path)
            except Exception as e:
                pass  
    return setuid_files

def save_to_file(file_paths, output_file):
    with open(output_file, 'w') as f:
        for file_path in file_paths:
            f.write(file_path + '\n')

if __name__ == "_main_":
    setuid_files = find_setuid_files()
    if setuid_files:
        save_to_file(setuid_files, 'success.txt')
        print("Successful results saved to success.txt")
    else:
        print("No files with setuid bit set found.")
