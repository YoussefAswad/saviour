import requests
import yaml
import os
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

config = None

filename = os.getenv('env', 'manifest.yaml').lower()
script_dir = os.path.dirname(__file__)
abs_file_path = os.path.join(script_dir, filename)
file = requests.get(
    'https://raw.githubusercontent.com/mtkennerly/ludusavi-manifest/master/data/manifest.yaml')

# print(file.text)
config = yaml.load(file.text, Loader=Loader)
