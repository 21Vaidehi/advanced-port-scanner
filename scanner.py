from colorama import Fore, Style, init
import socket
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# Initialize colorama
init(autoreset=True)

# ==============================
# FAST MULTITHREADED PORT SCANNER
# ==============================

print(Fore.CYAN + "=" * 50)
print(Fore.YELLOW + "     FAST MULTITHREADED SCANNER")
print(Fore.CYAN + "=" * 50)

# User input
target = input(Fore.GREEN + "Enter Target: ")

start_port = int(input(Fore.GREEN + "Start Port: "))
end_port = int(input(Fore.GREEN + "End Port: "))

# Resolve hostname to IP
try:
    target_ip = socket.gethostbyname(target)

except socket.gaierror:
    print(Fore.RED + "\nInvalid hostname or website!")
    exit()

print(Fore.CYAN + f"\nScanning {target} ({target_ip})")
print(Fore.CYAN + f"Started at: {datetime.now()}")
print(Fore.CYAN + "=" * 50)

# Save results
file = open("scan_results.txt", "w")

# Common services dictionary
common_ports = {
    20: "FTP Data",
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    135: "MSRPC",
    139: "NetBIOS",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    3306: "MySQL",
    3389: "RDP"
}

# Scan function
def scan(port):

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Faster scanning timeout
        s.settimeout(0.1)

        result = s.connect_ex((target, port))

        # Open port found
        if result == 0:

            # Detect common service
            service = common_ports.get(port, "Unknown Service")

            output = f"[OPEN] Port {port} | {service}"

            print(Fore.GREEN + output)

            # Save to file
            file.write(output + "\n")

        s.close()

    except:
        pass

# Efficient multithreading
with ThreadPoolExecutor(max_workers=100) as executor:

    executor.map(scan, range(start_port, end_port + 1))

# Close file
file.close()

print(Fore.CYAN + "=" * 50)
print(Fore.RED + "Scan Completed!")
print(Fore.YELLOW + "Results saved in scan_results.txt")
print(Fore.CYAN + "=" * 50)