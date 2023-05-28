# System-Response-Analyzer


System Response Analyzer is a Python tool that measures the response time of a given URL and provides system information such as CPU and memory usage, available disk space, network statistics, and OS update status.

## Installation

You can install System Response Analyzer using `pip`:
pip install system-response-analyzer

## Usage

To run System Response Analyzer, execute the following command in your terminal:
system-response-analyzer

You will be prompted to enter the URL you want to measure the response time for.

The tool will display the following information:

- Response time for the provided URL
- CPU usage percentage
- Memory usage percentage
- Available disk space
- Network statistics (bytes sent and received)
- Operating system update status

## Examples

Measure response time for a website:
Enter the URL to measure response time: https://example.com

Measure response time for an IP address:
Enter the URL to measure response time: 192.168.0.1

Measure response time for the local host:
Enter the URL to measure response time: localhos


## Dependencies

System Response Analyzer depends on the following Python packages:

- requests
- psutil
- tabulate

These dependencies will be automatically installed when you install the tool using `pip`.

## License

This project is licensed under the [MIT License](LICENSE).

