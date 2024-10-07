import os
from dotenv import load_dotenv

load_dotenv()


def get_env_variable(key: str, default: str = None) -> str:
    """Helper function to get the environment variable or raise an error."""
    value = os.environ.get(key, default)
    if value is None:
        raise ValueError(f"Environment variable {key} not set and no default provided.")
    return value


config = {}

environment = os.environ.get('FAST_API_ENV', 'development').lower()

if environment == 'production':
    config['ADMIN_TOKEN'] = get_env_variable('PRODUCTION_ADMIN_TOKEN')
    config['ADZUNA_API_KEY'] = get_env_variable('PRODUCTION_ADZUNA_KEY')
    config['ADZUNA_ID'] = get_env_variable('PRODUCTION_ADZUNA_ID')
else:
    config['ADMIN_TOKEN'] = get_env_variable('TEST_ADMIN_TOKEN', 'default_test_admin_token')
    config['ADZUNA_API_KEY'] = get_env_variable('TEST_ADZUNA_KEY', 'default_test_adzuna_key')
    config['ADZUNA_ID'] = get_env_variable('TEST_ADZUNA_ID', 'default_test_adzuna_id')
