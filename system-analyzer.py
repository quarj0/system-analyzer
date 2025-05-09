import os
import subprocess
import sys
import requests
import platform
import psutil
import time
import logging
from tabulate import tabulate
from colorama import Fore, Style
from plyer import notification
import json
import speedtest
import cpuinfo

# Setup logging
logging.basicConfig(filename='system_analyzer.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

logging.info(f"System Analyzer started.")
logging.info(f"Analyzer started at: {time.ctime()}")
logging.info(f"Analyzer PID: {os.getpid()}")
logging.info(f"User: {os.getlogin()}")
logging.info(f"Platform: {platform.platform()}")


def is_raspberry_pi():
    try:
        with open('/proc/cpuinfo', 'r') as f:
            cpuinfo = f.read().lower()
            return 'raspberry pi' in cpuinfo or 'bcm' in cpuinfo
    except FileNotFoundError:
        return False


def measure_system_response(url):
    try:
        response = requests.get(url if url.startswith(
            "http") else f"http://{url}", timeout=15)
        return response.elapsed.total_seconds() * 1000
    except requests.RequestException as e:
        logging.error(f"Error measuring system response: {e}")
        return None


def check_os_updates():
    system = platform.system()
    try:
        if system == 'Linux':
            if is_raspberry_pi():
                print("Raspberry Pi detected. Checking for updates using apt.")
                if os.geteuid() != 0:
                    print(
                        "This script requires superuser privileges to check for updates.")
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
            upgrade_command = ['powershell', '-Command',
                               'Install-WindowsUpdate', '-AcceptAll']

        update_result = subprocess.run(
            update_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if update_result.returncode == 0:
            print("Updates are available for the operating system.")
            update_choice = input(
                "Do you want to update now? (yes/no): ").strip().lower()
            if update_choice == 'yes':
                upgrade_result = subprocess.run(
                    upgrade_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
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
        logging.error(f"Error checking for updates: {e}")
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


def colorize_usage(value, threshold):
    if value > threshold:
        return f"{Fore.RED}{value}%{Style.RESET_ALL}"
    return f"{Fore.GREEN}{value}%{Style.RESET_ALL}"


def get_system_info():
    cpu_info = cpuinfo.get_cpu_info()
    return {
        'OS': platform.system(),
        'OS Version': platform.version(),
        'Machine': platform.machine(),
        'Processor': cpu_info.get('brand_raw', 'Unknown Processor'),
        'Uptime': time.time() - psutil.boot_time(),
        'Is Raspberry Pi': is_raspberry_pi()
    }


def network_speed_test():
    valid_responses = ['yes', 'y', 'no', 'n']
    question = input(
        "Do you want to run a network speed test? (yes/no): ").strip().lower()
    attempts = 2
    while question not in valid_responses:
        attempts -= 1
        print(
            f"Invalid input. Please enter 'yes', 'no', 'y', or 'n'. Attempts remaining: {attempts}\n")
        question = input(
            "Do you want to run a network speed test? (yes/no): ").strip().lower()
        if attempts == 0:
            print("Max attempts reached. Skipping speed test.\n")
            return {
                'Download Speed (Mbps)': None,
                'Upload Speed (Mbps)': None
            }

    if question in ['no', 'n']:
        return {
            'Download Speed (Mbps)': None,
            'Upload Speed (Mbps)': None
        }
    else:
        print(f"Running network speed test. This may take a few minutes...\n")
        try:
            st = speedtest.Speedtest()
            download_speed = st.download() / 1_000_000
            upload_speed = st.upload() / 1_000_000
            return {
                'Download Speed (Mbps)': download_speed,
                'Upload Speed (Mbps)': upload_speed
            }
        except speedtest.ConfigRetrievalError as e:
            logging.error(f"Speedtest configuration error: {e}")
            print("Unable to retrieve speed test configuration. Skipping speed test.\n")
            return {
                'Download Speed (Mbps)': None,
                'Upload Speed (Mbps)': None
            }


def send_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=10
    )


def export_to_json(data, filename='results.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def present_results(cpu_usage, memory_usage, updates, response_time, disk_usage, network_info, system_info, speed_info):
    headers = ["Metric", "Value"]
    data = [
        ["CPU Usage", colorize_usage(cpu_usage, 75) + "%"],
        ["Memory Usage", colorize_usage(memory_usage, 75) + "%"],
        ["Updates Available", "Yes" if updates else "No"],
        ["Response Time", f"{response_time} ms" if response_time else "N/A"],
        ["Disk Usage", colorize_usage(disk_usage, 75) + "%"],
        ["KB Sent", f"{network_info['kilobytes_sent']:.2f} KB"],
        ["KB Received", f"{network_info['kilobytes_received']:.2f} KB"],
        ["Download Speed",
            f"{speed_info['Download Speed (Mbps)']:.2f} Mbps" if speed_info['Download Speed (Mbps)'] else "N/A"],
        ["Upload Speed",
            f"{speed_info['Upload Speed (Mbps)']:.2f} Mbps" if speed_info['Upload Speed (Mbps)'] else "N/A"],
        ["OS", system_info['OS']],
        ["OS Version", system_info['OS Version']],
        ["Processor", system_info['Processor']],
        ["Machine", system_info['Machine']],
        ["Raspberry Pi", "Yes" if system_info['Is Raspberry Pi'] else "No"],
        ["Uptime", f"{system_info['Uptime'] / 3600:.2f} hours"]
    ]
    print(tabulate(data, headers, tablefmt="grid"))


def main():
    try:
        url = sys.argv[1] if len(sys.argv) == 2 else input("Enter a URL: ")
        response_time = measure_system_response(url)
        if response_time is None:
            user_choice = input(
                "The URL is unreachable. Continue (C) or enter different URL (D)? ").strip().lower()
            if user_choice == 'c':
                print("Continuing with the rest of the script.")
            elif user_choice == 'd':
                new_url = input("Enter a different URL: ")
                response_time = measure_system_response(new_url)
                if response_time is None:
                    print("The URL cannot be reached. Check your network.")
                    sys.exit(1)
            else:
                print("Invalid choice. Exiting.")
                sys.exit(1)

        updates = check_os_updates()
        cpu_usage = get_cpu_usage()
        memory_usage = get_memory_usage()
        disk_usage = get_disk_usage()
        network_info = get_network_information()
        system_info = get_system_info()
        speed_info = network_speed_test()

        present_results(cpu_usage, memory_usage, updates, response_time,
                        disk_usage, network_info, system_info, speed_info)

        export_to_json({
            'cpu_usage': cpu_usage,
            'memory_usage': memory_usage,
            'disk_usage': disk_usage,
            'network_info': network_info,
            'system_info': system_info,
            'speed_info': speed_info,
            'response_time': response_time,
            'updates': updates
        })

        if cpu_usage > 75 or memory_usage > 75 or disk_usage > 75:
            send_notification(
                "High Resource Usage", f"CPU: {cpu_usage}%, Memory: {memory_usage}% Disk: {disk_usage}%")

    except KeyboardInterrupt:
        print("\nExiting system response analyzer...")
    except KeyError as e:
        print(f"Error: {e} is not a valid URL")


if __name__ == '__main__':
    main()
