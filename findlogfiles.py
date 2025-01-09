import subprocess

def save_logs(output_path):
    
    command = f"journalctl --since='2 weeks ago' > /home/cruzz/xoxo/Miniproject/Codes/system_logs.txt"
    
    try:
        
        subprocess.run(command, shell=True, check=True)
        print(f"System logs from the last two weeks have been saved to /home/cruzz/xoxo/Miniproject/Codes")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the command: {e}")

def main():
    
    output_path = '/home/cruzz/xoxo/Miniproject/Codes/system_logs.txt'  

    
    save_logs(output_path)

if __name__ == "__main__":
    main()

