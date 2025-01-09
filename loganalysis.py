import re
from datetime import datetime, timedelta


RED = "\033[31m"
RESET = "\033[0m"


malicious_patterns = [
    'authentication failure',
    'failed password',
    'malware',
    'suspicious activity',
    
]


malicious_regex = re.compile('|'.join(malicious_patterns), re.IGNORECASE)

def analyze_logs(file_path):
    
    timestamp_pattern = re.compile(r'^\w{3} \d{1,2} \d{2}:\d{2}:\d{2}')
    
    
    two_weeks_ago = datetime.now() - timedelta(weeks=2)
    
    
    with open(file_path, 'r') as f:
        
        for line in f:

            match = timestamp_pattern.search(line)
            if match:
                
                try:
                    log_time = datetime.strptime(match.group(), "%b %d %H:%M:%S")
                    
                    log_time = log_time.replace(year=datetime.now().year)
                except ValueError:
                    continue  
                
                if log_time >= two_weeks_ago:
                    
                    if malicious_regex.search(line):
                        
                        print(f"{RED}{line.strip()}{RESET}")
                    else:
                       
                        print(line.strip())

def main():
    
    log_file_path = '/home/cruzz/xoxo/Miniproject/Codes/system_logs.txt'  
    
    analyze_logs(log_file_path)

if __name__ == "__main__":
    main()

