import requests
from pathlib import Path
import validators
import json
import yaml
from datetime import date, datetime
try:
    from yaml import CBaseLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import BaseLoader as Loader, Dumper

# YAML


def read_yaml(file: str):
    if isinstance(file, Path):
        file = str(file)
    if validators.url(file):
        return read_yaml_url(file)
    elif Path(file).expanduser().is_file():
        return read_yaml_file(file)
    else:
        raise SystemExit(f"{file} is neither a valid path or url")


def read_yaml_data(data):
    try:
        return yaml.load(data, Loader=Loader)
    except Exception as e:
        print(f"{e}: There was an error parsing to yaml")


def read_yaml_file(filepath):
    with open(Path(filepath).expanduser()) as stream:
        return read_yaml_data(stream)


def read_yaml_url(url):
    try:
        data = requests.get(url).text
        return read_yaml_data(data)
    except requests.exceptions.Timeout:
        raise SystemExit(f'Connection to {url} timedout')
    except requests.exceptions.TooManyRedirects:
        raise SystemExit(f'Connection to {url} failed')
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)


def to_yaml(data, file):
    with open(Path(file).expanduser(), 'w') as yaml_file:
        yaml.dump(data, yaml_file, default_flow_style=False)

# JSON


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def read_json(file):
    if isinstance(file, Path):
        file = str(file)
    if validators.url(file):
        return read_json_url(file)
    elif Path(file).expanduser().is_file():
        return read_json_file(file)
    else:
        raise SystemExit(f"{file} is neither a valid path or url")


def read_json_data(data):
    try:
        return json.load(data)
    except Exception as e:
        print(f"{e}: There was an error parsing to json")


def read_json_file(filepath):
    with open(Path(filepath).expanduser()) as stream:
        return read_yaml_data(stream)


def read_json_url(url):
    try:
        data = requests.get(url).text
        return read_yaml_data(data)
    except requests.exceptions.Timeout:
        raise SystemExit(f'Connection to {url} timedout')
    except requests.exceptions.TooManyRedirects:
        raise SystemExit(f'Connection to {url} failed')
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)


def to_json(data, file):
    with open(Path(file).expanduser(), 'w') as json_file:
        json.dump(data, json_file, default=json_serial)


def create_regex(str):
    return ''.join([("[" + x.upper() + '|' + x.lower() + "]") if x.isalpha() else x for x in str])


def main():
    with open("../manifest.yaml") as file:
        read_yaml_data(file)


if __name__ == "__main__":
    main()
