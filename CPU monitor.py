import psutil
import time


def check_cpu_usage(threshold):
    while True:
        cpu_percent = psutil.cpu_percent(interval=1)
        if cpu_percent > threshold:
            print(f"High CPU usage detected! Current CPU usage: {cpu_percent}%")
            
        else:
            print(f"CPU usage is normal. Current CPU usage: {cpu_percent}%")
        time.sleep(5)  

def main():
    
    threshold = 80
    print(f"Monitoring CPU usage. Threshold set to {threshold}%\n")
    check_cpu_usage(threshold)

if __name__ == "__main__":
    main()
