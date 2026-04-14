import os
import datetime
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from scapy.all import sniff, IP, TCP

load_dotenv()

#Database Connection setup
DB_URI = os.getenv('DATABASE_URL')

if not DB_URI:
    print("[ERROR] DATABASE_URL not found in .env file!")
    exit(1)

try:
    engine = create_engine(DB_URI)
    # Quick connectivity test
    with engine.connect() as conn:
        pass
    print("[SUCCESS] Connected to PostgreSQL.")
except Exception as e:
    print(f"[ERROR] Database connection failed: {e}")
    exit(1)

BATCH_SIZE = 1 
packet_buffer = []

def process_packet(packet):
    global packet_buffer

    if packet.haslayer(IP) and packet.haslayer(TCP):
        # Create the data entry
        event = {
            'timestamp': datetime.datetime.now(),
            'src_ip': packet[IP].src,
            'dst_port': packet[TCP].dport,
            'tcp_flags': str(packet[TCP].flags),
            'payload_len': len(packet[TCP].payload),
            'packet_size': len(packet)
        }
        
        # Immediate terminal feedback
        print(f"[*] ATTACK DETECTED: {event['src_ip']} -> Port {event['dst_port']} (Flags: {event['tcp_flags']})")
        
        packet_buffer.append(event)

        if len(packet_buffer) >= BATCH_SIZE:
            try:
                # Convert to DataFrame and push to SQL
                df = pd.DataFrame(packet_buffer)
                df.to_sql('incident_logs', engine, if_exists='append', index=False)
                
                print(f"[!!!] DATABASE UPDATE: Recorded to 'incident_logs' table.\n")
                
                packet_buffer.clear()
            except Exception as e:
                print(f"[ERROR] Could not write to Database: {e}")

# BPF Filter String
# Watches specific ports regardless of destination IP
bpf_filter = "tcp and (port 22 or 23 or 80 or 445)"

def main():
    print("CPT IDS: LIVE TESTING MODE")
    print("Listening on Interface: Loopback (lo)")
    print("Filtering for Ports: 22 (SSH), 23 (Telnet), 80 (HTTP), 445 (SMB)")
    print("Waiting for traffic... (Press Ctrl+C to stop)")
    
    try:
        # iface="lo" ensures it catches traffic to 127.0.0.1
        sniff(iface="lo", filter=bpf_filter, prn=process_packet, store=0)
    except KeyboardInterrupt:
        print("\nStopping IDS. Goodbye!")

if __name__ == "__main__":
    main()
