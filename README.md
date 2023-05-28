# System-Response-Analyzer


System Response Analyzer is a Python tool that measures the response time of a given URL and provides system information such as CPU and memory usage, available disk space, network statistics, and OS update status.

## Installation

Cloning the Repo
git clone https://github.com/hacks-and-codes/System-Response-Analyzer

You can install System Response Analyzer using `pip`:
pip install system-response-analyzer

## Usage

To run System Response Analyzer, execute the following command in your terminal:

python system-response-analyzer.py

You will be prompted to enter the URL you want to measure the response time for.

The tool will display the following information:

- Response time for the provided URL
- CPU usage percentage
- Memory usage percentage
- Disk Space used percentage
- Network statistics (bytes sent and received)
- Operating system update status

## Examples

Measure response time for a website:
Enter the URL to measure response time: example.com

Measure response time for an IP address:
Enter the URL to measure response time: 192.168.0.1

Measure response time for the local host:
Enter the URL to measure response time: localhost

Measure response time for the local host:
Enter the URL to measure response time: 127.0.0.1


## Dependencies

System Response Analyzer depends on the following Python packages:

- requests
- psutil
- tabulate

These dependencies will be automatically installed when you install the tool using `pip`.

## License

This project is licensed under the [MIT License](LICENSE).

