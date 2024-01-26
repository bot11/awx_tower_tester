import requests

class AWXAuthenticator:
    def __init__(self, api_url, username, password):
        self.api_url = api_url
        self.username = username
        self.password = password
        self.headers = {'Content-Type': 'application/json'}

    def get_auth_token(self):
        auth_endpoint = f"{self.api_url}/authtoken/"
        payload = {
            'username': self.username,
            'password': self.password
        }
        try:
            response = requests.post(auth_endpoint, json=payload)
            response.raise_for_status()
            self.headers['Authorization'] = f"Bearer {response.json()['token']}"
            return response.json()['token']
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return None
        except Exception as err:
            print(f"An error occurred: {err}")
            return None

    def get_job_template_id(self, job_template_names):
        job_templates_endpoint = f"{self.api_url}/job_templates/"
        response = requests.get(job_templates_endpoint, headers=self.headers)
        
        try:
            response.raise_for_status()
            job_templates_data = response.json()
            
            if 'results' not in job_templates_data:
                raise ValueError("Malformed response: missing 'results' key")
            
            job_template_mapping = {
                job_template['name']: job_template['id']
                for job_template in job_templates_data['results']
                if 'name' in job_template and 'id' in job_template
            }
            
            job_template_ids = {}
            for name in job_template_names:
                if name in job_template_mapping:
                    job_template_ids[name] = job_template_mapping[name]
                else:
                    raise ValueError(f"Job template name '{name}' does not exist.")
            
            return job_template_ids
            
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            raise
        except Exception as err:
            print(f"An error occurred: {err}")
            raise