#To find Abnormal Connection in the network
import csv
import psutil
import time
import argparse


def check_network_connections(output_file_path):
    
    with open(output_file_path, 'w', newline='') as csvfile:
       
        fieldnames = ['Local Address', 'Remote Address', 'PID']
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()

       
        while True:
            
            connections = psutil.net_connections()
            
            for conn in connections:
                
                if conn.status == 'ESTABLISHED' and conn.pid:
                    
                    writer.writerow({'Local Address': conn.laddr, 'Remote Address': conn.raddr, 'PID': conn.pid})
                    

            
            time.sleep(5)  

def main():
    
    parser = argparse.ArgumentParser(description="Monitor network connections for abnormal activity.")
    
    parser.add_argument("output_file_path", type=str, help="Path to the output CSV file where network connections data will be saved.")
    
    
    args = parser.parse_args()
    
    
    print("Monitoring network connections for abnormal activity...\n")
    
    
    check_network_connections(args.output_file_path)


if __name__ == "__main__":
    main()



#python3 Abnormalconnection.py /home/cruzz/xoxo/Miniproject/Codes/network_connections.csv
