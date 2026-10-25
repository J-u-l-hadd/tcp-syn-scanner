from scapy.all import IP, TCP, ICMP ,sr
import argparse
import socket
import sys
from pathlib import Path
from datetime import datetime

start = datetime.now()
start_time = start.strftime("%Y-%m-%d %H:%M:%S")
##setting up the argument parser
parser = argparse.ArgumentParser(description="Custom TCP SYN Scanner")
parser.add_argument("target", help="The target IP address to scan")
parser.add_argument("-p", "--ports", default=None, help="Port range to scan (default: 1-65535)")
args = parser.parse_args()


# Getting the prot range from the user input
if args.ports is None:
    target_ports = (0, 65535)
elif '-' in args.ports:
    string_parts = args.ports.split('-')  
    start_port = int(string_parts[0])
    end_port = int(string_parts[1])
    target_ports = (start_port, end_port)
elif ',' in args.ports:
    string_parts = args.ports.split(',')  
    target_ports = [int(port) for port in string_parts]
else :
    target_ports = int(args.ports)


##Host name resolution
##Cleaning
raw_target = args.target
if "://" in raw_target:
    raw_target = raw_target.split("://")[1]
if "/" in raw_target:
    clean_hostname = raw_target.split("/")[0]
else:
    clean_hostname = raw_target

##looking up the IP address
try:
    target_ip = socket.gethostbyname(clean_hostname)
    print(f"Target acquired: {target_ip}\n")
except socket.gaierror:
    print("Error: Could not resolve that hostname.")
    sys.exit(1)



##Creating the packets
ip_layer = IP(dst=target_ip)
tcp_layer = TCP(dport=target_ports, flags='S')
probe = ip_layer / tcp_layer
##probe.show()


##Sending the packets and receiving the responses
print(f"Scanning ports from {target_ports} on target {target_ip}")
answered, unanswered = sr(probe, timeout=2, verbose=False)
print(f"Got answers from {len(answered)} ports.\n")


##Reading results 
open_ports = []
closed = []
filtered = []
##unanswered packets are considered filtered
for sent in unanswered:
    filtered.append(sent[TCP].dport)
##answered packets are checked for open or closed ports
for sent, received in answered:
    if received.haslayer(TCP):
        if received.getlayer(TCP).flags == "SA":
            open_ports.append([sent[TCP].dport,(received.time-sent.time)*1000])
        elif "R" in received.getlayer(TCP).flags:
            closed.append([sent[TCP].dport,(received.time-sent.time)*1000])
    elif received.haslayer(ICMP):
        filtered.append(sent[TCP].dport)


##Processing time calculations
end_of_scan = datetime.now()
end_time = end_of_scan.strftime("%Y-%m-%d %H:%M:%S")
duration = str(end_of_scan - start)
if '.' in duration:
    base, ms = duration.split('.')
    duration = f"{base}.{ms[:4]}"


##Report generating
port_str = args.ports if args.ports else "all"
filename = f"scan_{clean_hostname}_{port_str}_{end_of_scan.strftime('%Y%m%d_%H%M%S')}.txt"
report_path = Path.cwd() / filename

print(f"Saving report to: {report_path}\n")
print(f"Scan complete for target {target_ip} \nTotal ports scanned: {len(open_ports) + len(closed) + len(filtered)} \nScanned ports: {target_ports} \nOpen ports: {len(open_ports)} \tClosed ports: {len(closed)} \tFiltered ports: {len(filtered)}\n")


with open(report_path, "w") as report_file:
    report_file.write(f"Started at {start_time}\tEnded at {end_time}\tDuration:{duration}\n")
    report_file.write(f"Scan complete for target {target_ip} \nTotal ports scanned: {len(open_ports) + len(closed) + len(filtered)} \nScanned ports: {target_ports} \nOpen ports: {len(open_ports)} \tClosed ports: {len(closed)} \tFiltered ports: {len(filtered)}\n")
    
    report_file.write("\nOpen ports: \nPort\tLatency\n")
    print("\nOpen ports: \nPort\tLatency")
    for port, latency in open_ports:
        report_file.write(f"{port} \t {latency:.2f} ms\n")
        print(f"{port} \t {latency:.2f} ms")
    
    print("\nClosed ports: \nPort\tLatency")
    report_file.write("\nClosed ports: \nPort\tLatency\n")
    for port, latency in closed:
        report_file.write(f"{port} \t {latency:.2f} ms\n")
        print(f"{port} \t {latency:.2f} ms")
    
    print("\nFiltered ports:")
    report_file.write("\nFiltered ports:\n")
    for port in filtered:
        report_file.write(f"Port {port} is filtered\n")
        print(f"Port {port} is filtered")
print(f"\nReport Saved")