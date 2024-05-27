import os
import subprocess
import sys
import requests
import platform
import psutil
from tabulate import tabulate


def measure_system_response(url):
    try:
        response = requests.get(url if url.startswith("http") else f"http://{url}", timeout=15)
        return response.elapsed.total_seconds() * 1000
    except requests.RequestException as e:
        print(f"Error measuring system response: {e}\n\n")
        return None


def check_os_updates():
    system = platform.system()
    try:
        if system == 'Linux':
            if platform.machine() == 'armv7l':
                print("Raspberry Pi detected. Checking for updates using apt.")
                if os.geteuid() != 0:
                    print("This script requires superuser privileges to check for updates.")
                    print("Please run the script with 'sudo'.")
                    return False
                update_command = ['apt', 'update', '-qq']
                upgrade_command = ['apt', 'upgrade', '-y']
            else:
                print("Linux detected. Checking for updates using apt.")
                update_command = ['apt-get', 'update', '-qq']
                upgrade_command = ['apt-get', 'upgrade', '-y']

        elif system == 'Darwin':
            print("MacOS detected. Checking for updates using softwareupdate.")
            update_command = ['softwareupdate', '-l']
            upgrade_command = ['softwareupdate', '-i', '-a']

        elif system == 'Windows':
            print("Windows detected. Checking for updates using Windows Update.")
            update_command = ['powershell', '-Command', 'Get-WindowsUpdate']
            upgrade_command = ['powershell', '-Command', 'Install-WindowsUpdate', '-AcceptAll']

        update_result = subprocess.run(update_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if update_result.returncode == 0:
            print("Updates are available for the operating system.")
            update_choice = input("Do you want to update now? (yes/no): ").strip().lower()
            if update_choice == 'yes':
                upgrade_result = subprocess.run(upgrade_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if upgrade_result.returncode == 0:
                    print("Updates were successfully installed.")
                else:
                    print("Error installing updates:")
                    print(upgrade_result.stderr)
            else:
                print("No updates were installed.")
            return True
        else:
            print("The operating system is up to date.")
            return False
    except Exception as e:
        print("Error checking for updates:")
        print(e)
        return False


def get_cpu_usage():
    return psutil.cpu_percent()


def get_memory_usage():
    return psutil.virtual_memory().percent


def get_disk_usage():
    return psutil.disk_usage('/').percent


def get_network_information():
    network = psutil.net_io_counters()
    return {
        'kilobytes_sent': network.bytes_sent / 1024,
        'kilobytes_received': network.bytes_recv / 1024
    }


def present_results(cpu_usage, memory_usage, updates, response_time, disk_usage, network_info):
    headers = ["Metric", "Value"]
    data = [
        ["CPU Usage", f"{cpu_usage}%"],
        ["Memory Usage", f"{memory_usage}%"],
        ["Updates Available", "Yes" if updates else "No"],
        ["Response Time", f"{response_time} ms" if response_time else "N/A"],
        ["Disk Usage", f"{disk_usage}%"],
        ["KB Sent", f"{network_info['kilobytes_sent']:.2f} KB"],
        ["KB Received", f"{network_info['kilobytes_received']:.2f} KB"]
    ]
    print(tabulate(data, headers, tablefmt="grid"))


def main():
    try:
        url = sys.argv[1] if len(sys.argv) == 2 else input("Enter a URL: ")

        response_time = measure_system_response(url)
        if response_time is None:
            user_choice = input("The URL is unreachable. Do you want to continue (C) or enter a different URL (D)? ").strip().lower()
            if user_choice == 'c':
                print("Continuing with the rest of the script.")
            elif user_choice == 'd':
                new_url = input("Enter a different URL: ")
                response_time = measure_system_response(new_url)
                if response_time is None:
                    print("The URL cannot be reached. Check if your network is working and try again.")
                    sys.exit(1)
                else:
                    print(f"Response time for {new_url}: {response_time} ms")
            else:
                print("Invalid choice. Exiting.")
                sys.exit(1)
        else:
            print(f"Response time for {url}: {response_time} ms")

        updates = check_os_updates()

        cpu_usage = get_cpu_usage()
        memory_usage = get_memory_usage()
        disk_usage = get_disk_usage()
        network_info = get_network_information()

        present_results(cpu_usage, memory_usage, updates, response_time, disk_usage, network_info)
    except KeyboardInterrupt:
        print("\nExiting system response analyzer...")
    except KeyError as e:
        print(f"Error: {e} is not a valid URL")


if __name__ == '__main__':
    main()
