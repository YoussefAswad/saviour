from dataclasses import dataclass
from pathlib import Path
import rw


@dataclass
class config:
    windows_mount: Path = None
    windows_users: list[str] = None
    prefixes: list[Path] = None
    custom_games: dict[str, list[Path]] = None

    def verify_config(self, conf):
        if 'windows_mount' not in conf:
            raise ValueError("windows_mount not found in config")
        if 'windows_users' not in conf:
            raise ValueError("windows_users not found in config")
        if 'prefixes' not in conf:
            raise ValueError("prefixes not found in config")
        if 'custom_games' not in conf:
            raise ValueError("custom_games not found in config")
        if not isinstance(conf['windows_mount'], str) or not conf['windows_mount']:
            raise ValueError("windows_mount must be a string")
        if not isinstance(conf['windows_users'], list) or not conf['windows_users']:
            raise ValueError("windows_users must be a list")
        if not isinstance(conf['prefixes'], list) or not conf['prefixes']:
            raise ValueError("prefixes must be a list")
        if not isinstance(conf['custom_games'], dict) or not conf['custom_games']:
            raise ValueError("custom_games must be a dict")
        for k, v in conf['custom_games'].items():
            if not isinstance(k, str):
                raise ValueError("custom_games keys must be strings")
            if not isinstance(v, list):
                raise ValueError("custom_games values must be a list")
            for p in v:
                if not isinstance(p, str):
                    raise ValueError("custom_games values must be strings")

    def read(self, file):
        conf = rw.read_yaml(file)
        self.verify_config(conf)
        self.windows_mount = Path(conf['windows_mount']).expanduser()
        if not self.windows_mount.is_absolute():
            raise ValueError("windows_mount must be an absolute path")
        self.windows_users = conf['windows_users']
        self.prefixes = [Path(p).expanduser() for p in conf['prefixes']]
        self.custom_games = conf['custom_games']
        for k, v in self.custom_games.items():
            self.custom_games[k] = [
                str((Path(p).relative_to(Path(p).anchor)).expanduser()) for p in v]

    def get_real_paths(self):
        new_conf = {}
        for game, paths in self.custom_games.items():
            new_paths = [rw.create_regex(x) for x in paths]
            new_conf[game] = new_paths
        return new_conf


def main():
    conf = config()
    conf.read("../config.yaml")
    print(conf)


if __name__ == '__main__':
    main()
