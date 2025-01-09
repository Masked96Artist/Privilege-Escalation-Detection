import csv
import re

def detect_abnormal_activity(bash_history_file, csv_output_file):
   
    abnormal_patterns = [
        r"sudo .*",  
        r"rm .*",    
        r"chmod .*", 
        
    ]
    
    
    abnormal_regex = re.compile('|'.join(abnormal_patterns), re.IGNORECASE)
    
    
    with open(bash_history_file, 'r') as history_file:
        
        with open(csv_output_file, 'w', newline='') as csv_file:

            writer = csv.writer(csv_file)
            
            writer.writerow(["Command", "Abnormal Behavior"])
            
            
            for line in history_file:
                line = line.strip()
                
                
                if abnormal_regex.search(line):
                    
                    writer.writerow([line, "Potential abnormal behavior detected"])
    
    print(f"Abnormal activity has been saved to {csv_output_file}")

def main():
    
    bash_history_file = 'bash_history.txt' 
    csv_output_file = 'abnormal_activity.csv' 
    detect_abnormal_activity(bash_history_file, csv_output_file)

if __name__ == "_main_":
    main()