import subprocess
import pyshark


capture_file_path = 'network_capture.pcap'
packet_count = 2000


def capture_network_traffic():
    try:
        
        subprocess.run(
            ['tshark', '-c', str(packet_count), '-w', capture_file_path],
            check=True
        )
        print(f"Network traffic captured and saved to {capture_file_path}")
    except subprocess.CalledProcessError as e:
        print("Error capturing network traffic:", e)


def analyze_capture_file():
    
    capture = pyshark.FileCapture(capture_file_path)

    
    for packet in capture:
        
        if hasattr(packet, 'ip'):
            if int(packet.ip.hdr_len) != 20: 
                print(f"Malformed packet: {packet.ip} - IP header length: {packet.ip.hdr_len}")

        


def main():
    
    capture_network_traffic()

    
    analyze_capture_file()

if __name__ == "__main__":
    main()

