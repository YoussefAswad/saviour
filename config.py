import yaml
import os

config = None

filename = os.getenv('env', './saviour/manifest/data.yml').lower()
script_dir = os.path.dirname(__file__)
abs_file_path = os.path.join(script_dir, filename)
with open(abs_file_path, 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
