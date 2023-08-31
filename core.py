import os
from pathlib import Path
import config


def verifyKey(key):
    return key in config.config and config.config[key] and len(config.config[key]) != 0


def parse_config():
    target_map = []
    if not verifyKey("windows_mount"):
        raise Exception("No path to windows mount point specified in config.")
    windows_users = config.config['windows_mount'] + "/Users"

    if not verifyKey("prefixes"):
        raise Exception("No path to a wine prefix was specified in config.")
    prefixes = config.config['prefixes']

    if not verifyKey("targets"):
        raise Exception("No targets were specified.")
    targets = config.config['targets']

    target_users = [os.getenv('USER'), 'steamuser']

    if verifyKey("additional_users"):
        target_users.extend(config.config['additional_users'])

    for target in targets:
        user = target['user']
        for path in target["paths"]:
            source = Path(windows_users + "/" + user + "/" + path)
            if source.exists():
                for prefix in prefixes:
                    for target_user in target_users:
                        if user == "Public":
                            target_user = "Public"
                        destination = Path(
                            prefix + '/drive_c/users/' + target_user + "/" + path)
                        curr_map = [source, destination.expanduser()]
                        if curr_map not in target_map:
                            target_map.append(curr_map)
            else:
                print(source.stem + " does not exist.")
    return (target_map)


def link(target_map):
    for curr_map in target_map:
        source = curr_map[0]
        destination = curr_map[1]

        if destination.exists():
            if destination.is_symlink():
                print("Skipped " + destination.stem)
                continue
            print(destination /
                  " already exists, try deleting or moving it and try agian!")
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.symlink_to(source)
            print("linked " + destination.stem)


def main():
    link(parse_config())


if __name__ == "__main__":
    main()
