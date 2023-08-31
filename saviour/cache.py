import re
# import manifest
import os
from dataclasses import asdict, dataclass
from pathlib import Path
import dateutil.parser
from datetime import datetime
import requests
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


import rw


if os.getenv("XDG_CACHE_HOME"):
    cache_dir = Path(os.getenv("XDG_CACHE_HOME")) / "saviour"
else:
    cache_dir = Path.home() / '.cache/saviour'


@dataclass
class manifest:
    mapping: dict = None
    timestamp: datetime = None
    url: str = 'https://raw.githubusercontent.com/mtkennerly/ludusavi-manifest/master/data/manifest.yaml'

    def get(self):
        self.mapping = parse_manifest(rw.read_yaml(self.url))
        self.timestamp = datetime.now()

    def read(self, file):
        file = rw.read_json(file)
        if self.verify(file):
            self.mapping = file['mapping']
            self.timestamp = dateutil.parser.isoparse(file['timestamp'])
            self.url = file['url']
        else:
            raise ValueError(
                f"The schema of the file provided is incomaptible, {type(file)} was given.")

    def write(self, file):
        rw.to_json(asdict(self), file)

    def update(self, force=False):
        if force:
            self.get()
            return True
        if (datetime.now() - self.timestamp).seconds / (60 * 60) < 3:
            return False
        res = requests.get(
            'https://api.github.com/repos/mtkennerly/ludusavi-manifest/commits/master')

        latest_commit_date = dateutil.parser.isoparse(
            res.json()['commit']["committer"]['date'])
        if self.timestamp.isoformat() < latest_commit_date.isoformat():
            self.get()
            return True
        return False

    def verify(self, data):
        if not isinstance(data, dict):
            return False
        if 'mapping' not in data or 'timestamp' not in data or 'url' not in data:
            return False
        return True

    def get_real_path(self, path: str, user: str) -> str:
        if path[0] == '/':
            path = path[1:]
        path = path.replace('<home>', 'Users/' + user)
        path = path.replace('<osUserName>', user)
        path = path.replace(
            '<winAppData>', 'Users/' + user + '/AppData/Roaming')
        path = path.replace(
            '<winLocalAppData>', 'Users/' + user + '/AppData/Local')
        path = path.replace(
            '<winDocuments>', 'Users/' + user + '/Documents')
        path = path.replace(
            '<winPublic>', 'Users/Public')
        path = path.replace(
            '<winProgramData>', 'ProgramData')
        path = path.replace(
            '<storeUserId>', '*')
        return rw.create_regex(path)

    def get_real_paths(self, windows_users: list[str]) -> dict:
        real_mapping = {}
        for game, paths in self.mapping.items():
            real_paths = []
            for path in paths:
                for user in windows_users:
                    new_path = self.get_real_path(str(path), user)
                    if new_path not in real_paths:
                        real_paths.append(new_path)
            real_mapping[game] = real_paths
        return real_mapping


# def get_manifest_yaml(url):
#     file = requests.get(url)
#     return yaml.load(file.text, Loader=Loader)


# def update_cache():

#     manifest_cache = rw.read_json(cache_dir)
#     res = requests.get(
#         'https://api.github.com/repos/mtkennerly/ludusavi-manifest/commits/master')

#     latest_commit_date = dateutil.parser.isoparse(
#         res.json()['commit']["committer"]['date'])
#     # if dateutil.parser.isoparse(cache_dir['time']) >=

#     manifest_raw = get_manifest_yaml(manifest_url)
#     manifest_parsed = parse_manifest(manifest_raw)
#     cache_dir.mkdir(parents=True, exist_ok=True)
#     manifest_cache_path = cache_dir / "cache.yaml"
#     with open(str(manifest_cache_path), 'w') as outfile:
#         yaml.dump(manifest_parsed, outfile,
#                   default_flow_style=False, Dumper=Dumper)
#     pass


def parse_manifest(data):
    exclude_list = ['<root>', '<base>', '<xdgData>', '<xdgConfig>']
    result = {}
    for k, v in data.items():
        if 'files' in v:
            locs = []
            for loc, info in v['files'].items():
                if 'tags' in info and 'save' in info['tags'] and \
                        not any([x in loc for x in exclude_list]):
                    while '**' in loc:
                        loc = loc.replace('**', '*')
                    loc = loc.replace('<storeUserId>', '*')
                    locs.append(loc)
            if locs:
                result[k] = locs
    return result


def main():
    # file = rw.read_yaml(str(cache_dir / "cache.yaml"))
    # new_cache = {"mapping": file, 'timestamp': datetime.now(
    # ), 'url': 'https://raw.githubusercontent.com/mtkennerly/ludusavi-manifest/master/data/manifest.yaml'}
    # rw.to_json(new_cache, cache_dir / "cache.json")

    man = manifest()
    man.read((cache_dir / "cache.json"))

    print(man.update())
    print(asdict(man))
    man.write(cache_dir / "new.json")
    # print(man.verify(man.asdict()))


if __name__ == '__main__':
    main()

# user = 'youssef'
# mount = '/mnt/Windows'
# mountp = Path(mount)
# for k, v in dict.items():
#     if 'files' in v:
#         locs = []
#         for loc, info in v['files'].items():
#             if 'tags' in info and 'save' in info['tags'] and \
#                     not any([x in loc for x in exclude_list]):
#                 # 'when' in info and {'os': 'windows'} in info['when'] and
#                 # while '*' in loc:
#                 #     loc = loc[:loc[:loc.find(
#                 #         '*')].rfind('/')]
#                 # if '/' not in loc:
#                 #     continue
#                 loc_comp = loc.replace('<home>', 'Users/' + user)
#                 loc_comp = loc_comp.replace('<osUserName>', user)
#                 loc_comp = loc_comp.replace(
#                     '<winAppData>', 'Users/' + user + '/AppData/Roaming')
#                 loc_comp = loc_comp.replace(
#                     '<winLocalAppData>', 'Users/' + user + '/AppData/Local')
#                 loc_comp = loc_comp.replace(
#                     '<winDocuments>', 'Users/' + user + '/Documents')
#                 loc_comp = loc_comp.replace(
#                     '<winPublic>', 'Users/Public')
#                 loc_comp = loc_comp.replace(
#                     '<winProgramData>', 'ProgramData')
#                 loc_comp = loc_comp.replace(
#                     '<storeUserId>', '*')
#                 if loc_comp[0] == '/':
#                     loc_comp = loc_comp[1:]
#                 # loc_comp = re.sub('\*+', '*', loc_comp)
#                 locs.append(loc_comp)
#         if locs:
#             result.append((k, locs))


# def create_regex(str):
#     return ''.join([("[" + x.upper() + '|' + x.lower() + "]") if x.isalpha() else x for x in str])


# inc = []
# for game in result:
#     paths = []
#     for path in game[1]:
#         # if game[0] == 'The Spectrum Retreat':
#         #     print(game[1])
#         # if '*' in path:
#         #     pg = glob.glob(path)
#         #     if pg:
#         #         paths.extend(pg)
#         # if os.path.exists(path):
#         #     paths.append(game)
#         # print(path)
#         if '<root>' in path:
#             print(path)
#         while '**' in path:
#             path = path.replace('**', '*')

#         pg = [x for x in mountp.glob(create_regex(path))]

#         if pg:
#             paths.extend(pg)
#     if paths:
#         inc.append((game[0], paths))

# dir_list = match.listallfiles(mount + "/Users")
# for game in result:
#     paths = []
#     for path in game[1]:
#         matched = match.match_path(path, dir_list)
#         if matched:
#             paths.extend(matched)
#     if paths:
#         inc.append((game[0], paths))

# for game in inc:
#     print(game[0])
# print(len(inc))
