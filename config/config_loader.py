from configparser import ConfigParser, NoSectionError, NoOptionError

class ConfigLoader:
    def __init__(self, config_file):
        self.config = ConfigParser()
        self.config.read(config_file)

    def get_config(self):
        config_data = {}
        try:
            config_data['api_url'] = self.config.get('config', 'api_url')
            config_data['api_username'] = self.config.get('config', 'api_username')
            config_data['api_password'] = self.config.get('config', 'api_password')
            config_data['job_log_dir'] = self.config.get('config', 'job_log_dir')
            config_data['target_hosts'] = self.config.get('defaults', 'target_hosts')
            config_data['jt_execution_order'] = self.config.get('jt_execution_order').split('\n')
            config_data['emails'] = self.config.get('report', 'emails')
            
            # SMTP configuration
            config_data['smtp_server'] = self.config.get('smtp', 'server')
            config_data['smtp_port'] = self.config.getint('smtp', 'port')
            config_data['smtp_username'] = self.config.get('smtp', 'username')
            config_data['smtp_password'] = self.config.get('smtp', 'password')
            
            # Load extra variables if they exist
            if 'extra_variables' in self.config:
                config_data['extra_variables'] = dict(self.config.items('extra_variables'))
            else:
                config_data['extra_variables'] = {}

        except NoSectionError as e:
            if str(e) != "No section: 'extra_variables'":
                raise ValueError(f"Missing section in configuration file: {e}")
        except NoOptionError as e:
            raise ValueError(f"Missing option in configuration file: {e}")

        for key, value in config_data.items():
            if isinstance(value, str) and not value.strip():
                raise ValueError(f"Configuration for '{key}' is empty.")
            if isinstance(value, list) and not all(item.strip() for item in value):
                raise ValueError(f"Configuration for '{key}' contains empty items.")

        return config_data