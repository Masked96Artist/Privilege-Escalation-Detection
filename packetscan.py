import pyshark 

capture_file_path = 'network_capture.pcap'


def analyze_capture_file():
    
    capture = pyshark.FileCapture(capture_file_path)

   
    for packet in capture:
        
        print(f"Packet Timestamp: {packet.sniff_time}")
        print(f"Protocol: {packet.highest_layer}")
        print(f"Source: {packet.ip.src}")
        print(f"Destination: {packet.ip.dst}")

       
        if hasattr(packet, 'ip'):
            if int(packet.ip.hdr_len) != 20:
                print(f"Malformed packet detected: {packet.ip}")

       
        print('-' * 40)


analyze_capture_file()

