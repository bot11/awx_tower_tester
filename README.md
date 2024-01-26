# awx_tester

awx_tester is a command-line interface (CLI) application written in Python, designed to automate the testing of job templates in Ansible Tower. It uses the Ansible Tower API to execute job templates, log their execution, and report the outcomes, aiming to streamline the testing process for developers.

## Features

- Executes Ansible Tower job templates in a specified order.
- Automatically stops or skips job execution on failure based on configuration.
- Saves job execution logs to a specified directory.
- Provides a summary report, including job statuses and logs, via email.

## Prerequisites

- Python 3.x
- Ansible Tower with accessible API

## Getting Started

Clone the repository and navigate into the project directory. Install the required dependencies with the command:

```
pip install -r requirements.txt
```

## Configuration

Edit the `config.ini` file to match your environment settings and job execution preferences. The configuration should include:

- Ansible Tower API credentials.
- Job execution directory path.
- Target hosts.
- Execution order of job templates, with optional `skip_on_failure` flags.
- Email settings for reporting.

```
[config]
api_url="https://awx-tower/v2/api"
api_username="your_username"
api_password="your_password"
job_log_dir="/path/to/job_logs/today_date_"

[defaults]
target_hosts="host1, host2"

[jt_execution_order]
job_template1
job_template2 - skip_on_failure
job_template3

[report]
emails="email@example.com"

[smtp]
server="your_smtp_server"
port=your_smtp_port
username="your_smtp_username"
password="your_smtp_password"
```

Ensure all placeholders are replaced with your actual data.

## Usage

To use awx_tester, run the following command:

```
python main.py -c /path/to/your/config.ini
```

## Development

The application's logic is split across several modules:

- `main.py`: The command-line interface handler and entry point.
- `config/config_loader.py`: Configuration file parser.
- `api/authenticator.py`: Handles AWX API authentication.
- `executors/job_executor.py`: Manages job template execution and reporting.
- `report/email_sender.py`: Sends execution summary via email.

## Contributing

Contributions are welcome. To contribute, please fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, raise an issue on the project's issue tracker or contact the project maintainers.