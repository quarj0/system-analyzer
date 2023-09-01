import os
import subprocess
import sys
import requests
import platform
import psutil
from tabulate import tabulate


def measure_system_response(url):
    try:
        if url.count(".") == 3:
            # Measure response time for IP addresses
            response = requests.get(f"http://{url}", timeout=15)
            return response.elapsed.total_seconds() * 1000
        elif url == "localhost" or url == "127.0.0.1":
            # Measure response time for local hostname
            response = requests.get("http://localhost", timeout=15)
            return response.elapsed.total_seconds() * 1000
        else:
            # Assume it's a website or API URL
            response = requests.get(f"http://{url}", timeout=15)
            return response.elapsed.total_seconds() * 1000
    except requests.RequestException as e:
        print(f"Error measuring system response: {e}\n\n")
        return None

def check_os_updates():
    system = platform.system()
    if system == 'Linux':
        # Add rasberry pi support
        if system == 'Linux' and platform.machine() == 'armv7l':
            print("Raspberry Pi detected. Checking for updates using apt.")

            try:
                # Check if the script is running with superuser privileges
                if os.geteuid() != 0:
                    print(
                        "This script requires superuser privileges to check for updates.")
                    print("Please run the script with 'sudo'.")
                    return False

                # Use subprocess to run the update command and capture the output
                command = ['apt', 'update', '-qq']
                update_result = subprocess.run(
                    command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                if update_result.returncode == 0:
                    # Updates are available, ask the user if they want to update
                    print("Updates are available for the operating system.")
                    update_choice = input(
                        "Do you want to update now? (yes/no): ").strip().lower()
                    if update_choice == 'yes':
                        update_command = ['apt', 'upgrade', '-y']
                        update_result = subprocess.run(
                            update_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                        if update_result.returncode == 0:
                            print("Updates were successfully installed.")
                        else:
                            print("Error installing updates:")
                            print(update_result.stderr)
                    else:
                        print("No updates were installed.")
                    return True
                else:
                    print("The operating system is up to date.")
                    return False
            except Exception as e:
                print("Error checking for updates:")
                print(e)
        # Add support for MacOS
        elif system == 'Darwin':
            print("MacOS detected. Checking for updates using softwareupdate.")
            try:
                command = ['softwareupdate', '-l']
                update_result = subprocess.run(
                    command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                if update_result.returncode == 0:
                    # Updates are available, ask the user if they want to update
                    print("Updates are available for the operating system.")
                    update_choice = input(
                        "Do you want to update now? (yes/no): ").strip().lower()
                    if update_choice == 'yes':
                        update_command = ['softwareupdate', '-i', '-a']
                        update_result = subprocess.run(
                            update_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                        if update_result.returncode == 0:
                            print("Updates were successfully installed.")
                        else:
                            print("Error installing updates:")
                            print(update_result.stderr)
                    else:
                        print("No updates were installed.")
                    return True
                else:
                    print("The operating system is up to date.")
                    return False
            except Exception as e:
                print("Error checking for updates:")
                print(e)
        # Add support for Windows
        elif system == 'Windows':
            print("Windows detected. Checking for updates using Windows Update.")
            try:
                command = ['powershell', 'Get-WindowsUpdate']
                update_result = subprocess.run(
                    command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                if update_result.returncode == 0:
                    # Updates are available, ask the user if they want to update
                    print("Updates are available for the operating system.")
                    update_choice = input(
                        "Do you want to update now? (yes/no): ").strip().lower()
                    if update_choice == 'yes':
                        update_command = ['powershell', 'Install-WindowsUpdate', '-AcceptAll']
                        update_result = subprocess.run(
                            update_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                        if update_result.returncode == 0:
                            print("Updates were successfully installed.")
                        else:
                            print("Error installing updates:")
                            print(update_result.stderr)
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
        'kilobytes_sent': network.bytes_sent / 1024,
        'kilobytes_received': network.bytes_recv / 1024
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
        ["KB Sent", f"{network_info['kilobytes_sent']:.2f} KB"],
        ["KB Received", f"{network_info['kilobytes_received']:.2f} KB"]
    ]
    print(tabulate(data, headers, tablefmt="grid"))


def main():
    try:
        if len(sys.argv) == 1:
            url = input("Enter a URL: ")
        elif len(sys.argv) == 2:
            url = sys.argv[1]
        else:
            print("Usage: python system-response-analyzer.py [URL]")
            sys.exit(1)

        response_time = measure_system_response(url)
        if response_time is None:
            user_choice = input(
                "The URL is unreachable. Do you want to continue (C) or enter a different URL (D)? ").strip().lower()
            if user_choice == 'c':
                print("Continuing with the rest of the script.")
            elif user_choice == 'd':
                new_url = input("Enter a different URL: ")
                response_time = measure_system_response(new_url)
                if response_time is None:
                    print(
                        "The URL cannot be reached. Check if your network is working and try again")
                    sys.exit(1)
                else:
                    print(
                        f"Response time for {new_url}: {response_time} seconds")
            else:
                print("Invalid choice. Exiting.")
                sys.exit(1)
        else:
            print(f"Response time for {url}: {response_time} seconds")

        updates = check_os_updates()
        if updates:
            print("OS Updates:")
            print(updates)
        else:
            pass

        cpu_usage = get_cpu_usage()
        memory_usage = get_memory_usage()
        disk_usage = get_disk_usage()
        network_info = get_network_information()

        present_results(cpu_usage, memory_usage, updates,
                        response_time, disk_usage, network_info)
    except KeyboardInterrupt:
        print("\nExiting system response analyzer...")
    except KeyError as e:
        print(f"Error: {e} is not a valid URL")


if __name__ == '__main__':
    main()
