

# System Analyser

A Python-based tool for measuring system response times, checking OS updates, monitoring system metrics like CPU, memory, disk usage, and network traffic, as well as conducting network speed tests.

![System Analyzer](./images/sysanalyzer.png)
<img src="./images/sysanalyzer.png" alt="System Response" width="500"/>

## Table of Contents

- [Installation](#installation)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Usage](#usage)
- [Examples](#examples)
- [Getting Started](#getting-started)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Installation

To install System Analyzer, follow the steps below:

### Cloning the Repository

```bash
git clone https://github.com/quarj0/system-analyzer
```

### Install Dependencies

First, install the required dependencies using:

```bash
pip install -r requirements.txt
```

Alternatively, install the tool via `pip` after packaging:

```bash
pip install system-analyzer
```

## Features

- **Response Time Measurement:** Measure response time for a given URL or IP address.
- **OS Update Check:** Check for available OS updates and provide upgrade options.
- **CPU & Memory Monitoring:** Track CPU and memory usage.
- **Disk Monitoring:** Monitor disk usage.
- **Network Monitoring:** Track network traffic (bytes sent and received).
- **Network Speed Test:** Test internet connection speeds.

## Prerequisites

Before using this tool, ensure that you have the following:

- Python 3.x installed.
- The following Python libraries:
  - `requests` (for making HTTP requests)
  - `psutil` (for system information)
  - `tabulate` (for pretty printing tables)

To install these, you can run:

```bash
pip install requests psutil tabulate
```

## Usage

To use the **System Analyzer**, follow these steps:

1. Clone the repository to your local machine.
2. Install the required dependencies (see [Prerequisites](#prerequisites)).
3. Run the script using the command:
   ```bash
   python system-analyzer.py [URL]
   ```
   If no URL or IP address is provided, the tool will prompt you to enter one.

4. Follow the on-screen instructions to get system metrics and network information.

### Logging
  - Tool will generate logs for further usage.
  This is done with json and with in-depth details in the log file.

![Generated system Analyzer log](https://github.com/quarj0/system-analyzer/blob/7b0420097ea35c566ee19cd52b542b8be6a6ac9f/sysanalyzerlog.png)
<img src="./images/sysanalyzerlog.png" alt="System Response log" width="500"/>

### Network Speed Testing
- The script will prompt whether you want to run a network speed test. You can choose 'yes' or 'no' as needed.

## Examples

### Measure response time for a website:
```bash
Enter the URL to measure response time: example.com
```

### Measure response time for an IP address:
```bash
Enter the URL to measure response time: 192.168.0.1
```

### Measure response time for the local host:
```bash
Enter the URL to measure response time: localhost
```

### Network Speed Test Prompt:
```bash
Do you want to run a network speed test? (yes/no): yes
```

## Getting Started

1. **Run the tool:** Start by running the script, optionally providing a URL/IP address.
2. **Check OS updates:** The tool will automatically check for updates and notify you if any are available.
3. **View metrics:** Once the tool runs, it will display system metrics like CPU usage, memory usage, disk space, network traffic, and more.
4. **Speed test:** You’ll be prompted to test your network speed.

## Dependencies

The System Analyzer relies on the following libraries:

- `psutil`: For gathering system-related information.
- `requests`: For making HTTP requests to check response times.
- `tabulate`: For formatting and displaying the data.
- `speedtest-cli`: For running network speed tests.
- `plyer`: For notifications.
- `cpuinfo`: For retrieving processor information.
- `colorama`: For adding color to terminal output.

## Contributing

Contributions are welcome! Feel free to fork this repository, open issues, or submit pull requests. Whether it's a bug fix, new feature, or improvement, your contribution will be appreciated.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for more details.
