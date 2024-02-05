from scapy.all import *
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

def calculate_throughput(packets, interval=1):
    throughput_data = []
    start_time = packets[0].time
    end_time = packets[-1].time
    current_time = start_time

    while current_time < end_time:
        current_interval_packets = [packet for packet in packets
                                     if current_time <= packet.time < current_time + interval]
        throughput = sum(len(packet) * 8 for packet in current_interval_packets) / interval / 1e6  # Convert to Mbps
        throughput_data.append({'Timestamp': current_time, 'Throughput': throughput})
        current_time += interval

    return pd.DataFrame(throughput_data)

def plot_throughput(dataframe, save_path=None):
    plt.plot(dataframe['Timestamp'].values, dataframe['Throughput'].values, label='Throughput')
    plt.xlabel('Time (sec)')
    plt.ylabel('Throughput (Mbps)')
    plt.title('Throughput Over Time')
    plt.legend()
    plt.savefig('graph.png')

def main():

    if len(sys.argv) != 3:
        print("Usage: python3 graph.py -f <pcap-file>")
        sys.exit(1)
        
    print("[+] Reading pcap file...")
    pcap_file = sys.argv[2]
    packets = rdpcap(pcap_file)
    print("[+] Pcap file read successfully!")

    # Calculate the throughput in Mbps/sec
    print("[+] Calculating throughput...")
    throughput_df = calculate_throughput(packets, interval=1)
    print("[+] Throughput calculated successfully!")

    # Create and save the plot
    print("[+] Creating plot...")
    plot_throughput(throughput_df)
    print("[+] Plot created successfully!")

if __name__ == "__main__":
    main()
