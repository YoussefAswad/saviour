import fnmatch
import re
from pathlib import Path


def listallfiles(path):
    return [x for x in Path(path).rglob('*')]


def match_path(path, dir_list):
    regex = fnmatch.translate(path)
    rec = re.compile(regex, re.IGNORECASE)
    return [i for i in dir_list if rec.match(str(i))]


def create_regex(str):
    return ''.join([("[" + x.upper() + '|' + x.lower() + "]") if x.isalpha() else x for x in str])
# dir_list = listallfiles('/mnt/Windows')

# path = '/mnt/Windows/Users/youssef/AppData/LocalLow/team Cherry/*dat'

# # regex = fnmatch.translate(path)
# # rec = re.compile(regex, re.IGNORECASE)

# # if (rec.match('/mnt/Windows/Users/youssef/Appdata/LocalLow/Team Cherry/user1.dat')):
# #     print('match')
# # else:
# #     print('no')

# # for i in dir_list:
# #     print(i)
# print(match_path(path, dir_list))
