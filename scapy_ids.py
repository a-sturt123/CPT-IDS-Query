import os
import datetime
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from scapy.all import sniff, IP, TCP

# 1. Load your .env file
load_dotenv()

# 2. Database Connection setup
DB_URI = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
engine = create_engine(DB_URI)

# 3. Settings
TARGET_IP = os.getenv('VM_IP')
BATCH_SIZE = 5
packet_buffer = []

def process_packet(packet):
    global packet_buffer

    if packet.haslayer(IP) and packet.haslayer(TCP):
        # Create the data entry
        event = {
            'timestamp': datetime.datetime.now(),
            'src_ip': packet[IP].src,
            'dst_port': packet[TCP].dport,
            'tcp_flags': packet[TCP].underlayer.sprintf("%TCP.flags%"),
            'payload_len': len(packet[TCP].payload),
            'packet_size': len(packet)
        }
        
        # --- PRINT 1: Immediate feedback for your test ---
        print(f"[*] ATTACK DETECTED: {event['src_ip']} -> Port {event['dst_port']} (Flags: {event['tcp_flags']})")
        
        packet_buffer.append(event)

        # 4. Batch Logic
        if len(packet_buffer) >= BATCH_SIZE:
            try:
                # Convert to DataFrame and push to SQL
                df = pd.DataFrame(packet_buffer)
                df.to_sql('incident_logs', engine, if_exists='append', index=False)
                
                # --- PRINT 2: Database confirmation ---
                print(f"\n[!!!] SUCCESS: Batch of {BATCH_SIZE} saved to PostgreSQL.\n")
                
                packet_buffer.clear()
            except Exception as e:
                print(f"[ERROR] Could not write to Database: {e}")

# 5. BPF Filter String
bpf_filter = f"tcp and dst host {TARGET_IP} and (port 22 or 23 or 80 or 445)"

def main():
    print("--- PROPRIETARY IDS: LIVE TESTING MODE ---")
    print(f"Targeting IP: {TARGET_IP}")
    print(f"Filtering for Ports: 22, 23, 80, 445")
    print("Waiting for traffic... (Press Ctrl+C to stop)")
    
    try:
        # Running the sniffer
        sniff(filter=bpf_filter, prn=process_packet, store=0)
    except KeyboardInterrupt:
        print("\nStopping IDS. Goodbye!")

if __name__ == "__main__":
    main()
