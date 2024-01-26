import argparse
import sys
from config.config_loader import ConfigLoader
from api.authenticator import AWXAuthenticator
from executors.job_executor import JobExecutor
from report.email_sender import EmailSender

def run_job_templates(config):
    auth = AWXAuthenticator(config['api_url'], config['api_username'], config['api_password'])
    auth_token = auth.get_auth_token()
    if not auth_token:
        print("Authentication failed. Exiting.")
        sys.exit(1)

    # Get job template IDs from their names
    job_template_names = [jt.split()[0] for jt in config['jt_execution_order']]
    job_template_ids_map = auth.get_job_template_id(job_template_names)

    # Replace job template names with job template IDs in the execution order
    config['jt_execution_order'] = [
        f"{job_template_ids_map[jt.split()[0]]} {' '.join(jt.split()[1:])}"
        for jt in config['jt_execution_order']
    ]

    executor = JobExecutor(auth_token, config['api_url'], config['job_log_dir'], job_template_ids_map)
    job_status_list = []
    for order_no, job_template in enumerate(config['jt_execution_order'], start=1):
        skip_on_failure = 'skip_on_failure' in job_template
        job_template_id = job_template.split()[0]

        try:
            print(f"Launching job template {job_template_id}")
            job_id = executor.launch_job_template(job_template_id)
            status = executor.poll_job_status(job_id)
            log_file_path = executor.save_job_log(job_id, job_template_id, order_no)
            print(f"Job {job_template_id} completed with status {status}. Log saved to {log_file_path}")

            job_status_list.append((job_template_id, status, log_file_path))

            if status != 'successful' and not skip_on_failure:
                print(f"Job {job_template_id} failed and is not marked to skip on failure. Exiting.")
                break

        except Exception as e:
            print(f"An exception occurred while running the job template {job_template_id}: {e}")
            job_status_list.append((job_template_id, 'failed', None))
            if not skip_on_failure:
                break

    send_summary_email(config, job_status_list)

def send_summary_email(config, job_status_list):
    email_subject = "AWX Tester Execution Summary"
    body_lines = ['AWX Tester execution completed. Summary:\n']
    for job_status in job_status_list:
        job_template, status, log_path = job_status
        line = f"- Job Template: {job_template}, Status: {status}, Log: {log_path}"
        body_lines.append(line)

    email_body = "\n".join(body_lines)
    email_sender = EmailSender(
        config['smtp_server'],
        config['smtp_port'],
        config['smtp_username'],
        config['smtp_password']
    )
    email_sender.send_email(email_subject, email_body, config['emails'])

def main():
    parser = argparse.ArgumentParser(description='awx_tester CLI application')
    parser.add_argument('-c', '--config', help='Path to the .ini configuration file', required=True)
    args = parser.parse_args()

    try:
        config_loader = ConfigLoader(args.config)
        config_data = config_loader.get_config()
        print("Configuration loaded successfully.")
        run_job_templates(config_data)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()