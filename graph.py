from scapy.all import *
import pandas as pd
import matplotlib.pyplot as plt
import os

def calculate_throughput(packets, interval=1):
    throughput_data = []
    start_time = packets[0].time
    end_time = packets[-1].time
    current_time = start_time

    while current_time < end_time:
        current_interval_packets = [packet for packet in packets
                                     if current_time <= packet.time < current_time + interval]
        throughput = sum(len(packet) * 8 for packet in current_interval_packets) / interval
        throughput_data.append({'Timestamp': current_time, 'Throughput': throughput})
        current_time += interval

    return pd.DataFrame(throughput_data)

def plot_throughput(dataframe, save_path=None):
    plt.plot(dataframe['Timestamp'].values, dataframe['Throughput'].values, label='Throughput')
    plt.xlabel('Time')
    plt.ylabel('Throughput (bps)')
    plt.title('Throughput Over Time')
    plt.legend()
    plt.savefig(save_path)

def main():
    print("[+] Reading pcap file...")
    pcap_file = "syn-flooding.pcapng"
    packets = rdpcap(pcap_file)
    print("[+] Pcap file read successfully!")


    # Calculate the throughput
    print("[+] Calculating throughput...")
    throughput_df = calculate_throughput(packets, interval=1)
    print("[+] Throughput calculated successfully!")

    # Create and save the plot
    print("[+] Creating plot...")
    home_directory = os.path.expanduser("~")
    save_path = os.path.join(home_directory, "graph.png")
    plot_throughput(throughput_df, save_path)
    print("[+] Plot created successfully and saved at home directory!")

if __name__ == "__main__":
    main()
