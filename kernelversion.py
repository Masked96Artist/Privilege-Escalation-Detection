import os
import subprocess

def check_kernel_version():
    
    kernel_version = subprocess.check_output(['uname', '-r']).decode().strip()
    print("Kernel version:", kernel_version)

def check_package_version(package_name):
    try:
        
        package_info = subprocess.check_output(['dpkg', '-s', package_name]).decode()
        version_line = [line for line in package_info.split('\n') if line.startswith('Version:')]
        if version_line:
            version = version_line[0].split(': ')[1].strip()
            print(f"{package_name} version:", version)
        else:
            print(f"Unable to find version information for {package_name}")
    except subprocess.CalledProcessError:
        print(f"Error: Unable to check version for {package_name}")

def main():
    print("Checking system components versions...\n")
    
   
    print("Checking kernel version...")
    check_kernel_version()
    print()

    
    packages_to_check = ['bash', 'openssl', 'libc6', 'libssl-dev']  # Add more packages as needed

   
    for package in packages_to_check:
        print(f"Checking {package} version...")
        check_package_version(package)
        print()

if __name__ == "__main__":
    main()