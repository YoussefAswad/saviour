from dataclasses import dataclass
from pathlib import Path
from config import config
from cache import manifest
import os


def get_config_path() -> Path:
    if os.getenv("XDG_CONFIG_HOME"):
        config_dir = Path(os.getenv("XDG_CONFIG_HOME")) / "saviour"
    else:
        config_dir = Path.home() / '.config/saviour'
    return config_dir / 'config.yaml'


def get_cache_path() -> Path:
    if os.getenv("XDG_CACHE_HOME"):
        cache_dir = Path(os.getenv("XDG_CACHE_HOME")) / "saviour"
    else:
        cache_dir = Path.home() / '.cache/saviour'
    return cache_dir


def create_regex(str):
    return ''.join([("[" + x.upper() + '|' + x.lower() + "]") if x.isalpha() else x for x in str])


class saviour:
    def __init__(self, config_file: Path = None, cache_dir: Path = None):
        self.windows_mount = None
        self.windows_users = None
        self.prefixes = None
        self.mapping = None

       # verify config file exists
        if not config_file:
            config_file = get_config_path()
        if not config_file.exists():
            raise FileNotFoundError(
                "Config file not found at " + str(config_file))
        # read config
        conf = config()
        conf.read(config_file)

        # verify cache exists
        if not cache_dir:
            cache_dir = get_cache_path()
        if not cache_dir.exists():
            cache_dir.mkdir(parents=False, exist_ok=True)
        # read/create manifest cache
        man = manifest()
        if not (cache_dir / 'manifest.json').exists():
            man.get()
        else:
            man.read(cache_dir / 'manifest.json')
        man.update()
        man.write(cache_dir / 'manifest.json')

        # verify windows_mount exists
        if not conf.windows_mount.is_dir():
            raise FileNotFoundError(
                "Windows mount not found at " + str(conf.windows_mount))
        # set windows_mount
        self.windows_mount = conf.windows_mount

        # verify given users exists in windows_mount
        for user in conf.windows_users:
            if not (self.windows_mount / 'Users' / user).is_dir():
                raise FileNotFoundError(
                    f"Windows user {user} not found in " + str(conf.windows_mount))
        # set windows_users
        self.windows_users = conf.windows_users

        # verfy given prefixes exists and are a valid wine prefix
        for prefix in conf.prefixes:
            if not prefix.is_dir():
                raise FileNotFoundError(
                    f"Prefix {prefix} not found at" + str(self.windows_mount))
            if not (prefix / 'drive_c').is_dir():
                raise FileNotFoundError(
                    f"Prefix {prefix} is not  wine prefix (does not contain a drive_c folder)")
        # set prefixes
        self.prefixes = conf.prefixes

        self.mapping = dict(man.get_real_paths(
            self.windows_users), **conf.get_real_paths())
        # new_conf = {}
        # for game, paths in conf.custom_games.items():
        #     new_paths = [create_regex(x) for x in paths]
        #     new_conf[game] = new_paths
        # self.mapping = dict(self.get_real_paths(
        #     man.mapping), **new_conf)

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
        return create_regex(path)

    def get_real_paths(self, mapping: dict) -> dict:
        for game, paths in mapping.items():
            real_paths = []
            for path in paths:
                for user in self.windows_users:
                    new_path = self.get_real_path(str(path), user)
                    if new_path not in real_paths:
                        real_paths.append(new_path)
            mapping[game] = real_paths
        return mapping

    def detect(self) -> dict[str, list[Path]]:
        res = {}
        for game, paths in self.mapping.items():
            new_paths = []
            for path in paths:
                # if game[0] == 'The Spectrum Retreat':
                #     print(game[1])
                # if '*' in path:
                #     pg = glob.glob(path)
                #     if pg:
                #         paths.extend(pg)
                # if os.path.exists(path):
                #     paths.append(game)
                # print(path)
                # if '<root>' in path:
                #     print(path)
                while '**' in path:
                    path = path.replace('**', '*')

                pg = [x for x in self.windows_mount.glob(path)]

                if pg:
                    new_paths.extend(pg)
            if new_paths:
                res[game] = [x.relative_to(self.windows_mount)
                             for x in new_paths]
        return res


def main():

    saveiour_instance = saviour()

    detected = saveiour_instance.detect()

    for game, paths in detected.items():
        print(f"{game} : {paths}")

    print(len(detected))


if __name__ == "__main__":
    main()
