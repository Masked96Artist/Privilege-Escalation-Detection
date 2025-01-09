import subprocess
import socket
import csv

def get_local_ip():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        
        return ip_address
    except socket.error as e:
        print("Error:", e)

def run_nmap(options, target, output_file):
    command = ["nmap"] + options.split() + [target]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        parsed_output = []
        lines = result.stdout.splitlines()
        for line in lines:
            if "/tcp" in line:  
                parts = line.split()
                port = parts[0].split("/")[0]
                state = parts[1]
                service = parts[2]
                parsed_output.append([port, state, service])

        with open(output_file, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Port', 'State', 'Service'])
            csv_writer.writerows(parsed_output)
        
        print("Nmap output written to", output_file)
        
    except subprocess.CalledProcessError as e:
        print("Error:", e)

options = "-A"
target = get_local_ip()
output_file = "nmap_output.csv"
run_nmap(options, target, output_file)
