def save_bash_history():
    
    home_directory = "/home/cruzz"  
    bash_history_path = f"{home_directory}/.zsh_history"
    
    
    output_file_path = "/home/cruzz/xoxo/Miniproject/Codes/bash_history.txt"
    
    try:
        
        with open(bash_history_path, "r", encoding="ISO-8859-1") as history_file:
            
            bash_history = history_file.readlines()
        
        
        with open(output_file_path, "w", encoding="UTF-8") as output_file:
            
            output_file.writelines(bash_history)
        
        print(f"Bash shell history has been saved to {output_file_path}")
    
    except Exception as e:
        print(f"An error occurred while accessing Bash history: {e}")

def main():
    save_bash_history()

if __name__ == "__main__":
    main()
