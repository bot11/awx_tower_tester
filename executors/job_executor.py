import os
import time
import requests
from datetime import datetime

class JobExecutor:
    def __init__(self, auth_token, api_url, job_log_dir, job_template_ids_map):
        self.auth_token = auth_token
        self.api_url = api_url
        self.job_log_dir = job_log_dir
        self.job_template_ids_map = job_template_ids_map
        self.headers = {'Authorization': f'Bearer {self.auth_token}'}

    def launch_job_template(self, job_template_name):
        job_template_id = self.job_template_ids_map.get(job_template_name)
        if job_template_id is None:
            raise ValueError(f"No job template found with name '{job_template_name}'")
        job_endpoint = f"{self.api_url}/job_templates/{job_template_id}/launch/"
        response = requests.post(job_endpoint, headers=self.headers)
        response.raise_for_status()
        return response.json()['job']

    def poll_job_status(self, job_id):
        job_detail_endpoint = f"{self.api_url}/jobs/{job_id}/"
        while True:
            response = requests.get(job_detail_endpoint, headers=self.headers)
            response.raise_for_status()
            status = response.json()['status']
            if status in ['successful', 'failed', 'error']:
                return status
            time.sleep(5)

    def save_job_log(self, job_id, job_template_name, order_no):
        logs_endpoint = f"{self.api_url}/jobs/{job_id}/stdout/"
        response = requests.get(logs_endpoint, headers=self.headers)
        response.raise_for_status()
        logs = response.text

        date_suffix = datetime.now().strftime('%Y%m%d')
        log_dir = f"{self.job_log_dir}{date_suffix}"
        os.makedirs(log_dir, exist_ok=True)

        log_file_path = os.path.join(log_dir, f"{order_no}_{job_template_name}.log")
        with open(log_file_path, 'w') as file:
            file.write(logs)

        return log_file_path