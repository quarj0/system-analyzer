import time
import requests
import subprocess
import platform
import psutil
from tabulate import tabulate


def measure_system_response(url):
    try:
        if url.startswith("http://") or url.startswith("https://"):
            # Measure response time for websites or APIs
            response = requests.get(url)
            return response.elapsed.total_seconds() * 1000
        elif url.count(".") == 3:
            # Measure response time for IP addresses
            response = requests.get(f"http://{url}")
            return response.elapsed.total_seconds() * 1000
        elif url == "localhost" or url == "127.0.0.1" :
            # Measure response time for local hostname
            response = requests.get("http://localhost")
            return response.elapsed.total_seconds() * 1000
        else:
            print("Invalid url type. Please enter a valid URL, IP address, or 'localhost'.")
    except requests.RequestException as e:
        print(f"Error measuring system response: {e}")
    return None



def check_os_updates():
    system = platform.system()
    if system == 'Linux':
        command = ['apt', 'update', '-qq']
        if subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
            return True
        else:
            return False
    elif system == 'Darwin':
        command = ['softwareupdate', '-l']
        if subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
            return True
        else:
            return False
    elif system == 'Windows':
        # Add Windows-specific update check logic here
        return False
    elif system == 'Linux' and platform.machine() == 'armv7l':
        # Raspberry Pi-specific update check logic
        # Implement the appropriate command or method for Raspberry Pi update checks
        return False
    else:
        return False


def get_cpu_usage():
    cpu_usage = psutil.cpu_percent()
    return cpu_usage


def get_memory_usage():
    memory = psutil.virtual_memory()
    memory_usage = memory.percent
    return memory_usage


def get_disk_usage():
    disk = psutil.disk_usage('/')
    disk_usage = disk.percent
    return disk_usage


def get_network_information():
    network = psutil.net_io_counters()
    network_info = {
        'bytes_sent': network.bytes_sent,
        'bytes_received': network.bytes_recv
    }
    return network_info


def present_results(cpu_usage, memory_usage, updates, response_time, disk_usage, network_info):
    headers = ["Metric", "Value"]
    data = [
        ["CPU Usage", f"{cpu_usage}%"],
        ["Memory Usage", f"{memory_usage}%"],
        ["Updates Available", "Yes" if updates else "No"],
        ["Response Time", f"{response_time} seconds"],
        ["Disk Usage", f"{get_disk_usage()}%"],
        ["Bytes Sent", f"{network_info['bytes_sent']}"],
        ["Bytes Received", f"{network_info['bytes_received']}"]    ]
    print(tabulate(data, headers, tablefmt="grid"))


def main():
    try:
        url = input("Enter the URL to measure response time: ")
        response_time = measure_system_response(url)
        if response_time:
            print(f"Response time for {url}: {response_time} seconds")
        else:
            print("An error occurred while measuring response time.")

        if check_os_updates():
            print("Updates are available for the operating system.")
        else:
            print("The operating system is up to date.")

        cpu_usage = get_cpu_usage()
        memory_usage = get_memory_usage()
        disk_usage = get_disk_usage()
        network_info = get_network_information()

        present_results(cpu_usage, memory_usage, check_os_updates(), response_time, disk_usage, network_info)
    except KeyboardInterrupt:
        print("\nExiting system response analyzer...")
if __name__ == '__main__':
    main()
