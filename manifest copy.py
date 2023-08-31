import re
import manifest
from pathlib import Path

dict = manifest.config

result = []

exclude_list = ['<root>', '<base>', '<xdgData>', '<xdgConfig>']


def update():
    pass


user = 'youssef'
mount = '/mnt/Windows'
mountp = Path(mount)
for k, v in dict.items():
    if 'files' in v:
        locs = []
        for loc, info in v['files'].items():
            if 'tags' in info and 'save' in info['tags'] and \
                    not any([x in loc for x in exclude_list]):
                # 'when' in info and {'os': 'windows'} in info['when'] and
                # while '*' in loc:
                #     loc = loc[:loc[:loc.find(
                #         '*')].rfind('/')]
                # if '/' not in loc:
                #     continue
                loc_comp = loc.replace('<home>', 'Users/' + user)
                loc_comp = loc_comp.replace('<osUserName>', user)
                loc_comp = loc_comp.replace(
                    '<winAppData>', 'Users/' + user + '/AppData/Roaming')
                loc_comp = loc_comp.replace(
                    '<winLocalAppData>', 'Users/' + user + '/AppData/Local')
                loc_comp = loc_comp.replace(
                    '<winDocuments>', 'Users/' + user + '/Documents')
                loc_comp = loc_comp.replace(
                    '<winPublic>', 'Users/Public')
                loc_comp = loc_comp.replace(
                    '<winProgramData>', 'ProgramData')
                loc_comp = loc_comp.replace(
                    '<storeUserId>', '*')
                if loc_comp[0] == '/':
                    loc_comp = loc_comp[1:]
                # loc_comp = re.sub('\*+', '*', loc_comp)
                locs.append(loc_comp)
        if locs:
            result.append((k, locs))


def create_regex(str):
    return ''.join([("[" + x.upper() + '|' + x.lower() + "]") if x.isalpha() else x for x in str])


inc = []
for game in result:
    paths = []
    for path in game[1]:
        # if game[0] == 'The Spectrum Retreat':
        #     print(game[1])
        # if '*' in path:
        #     pg = glob.glob(path)
        #     if pg:
        #         paths.extend(pg)
        # if os.path.exists(path):
        #     paths.append(game)
        # print(path)
        if '<root>' in path:
            print(path)
        while '**' in path:
            path = path.replace('**', '*')

        pg = [x for x in mountp.glob(create_regex(path))]

        if pg:
            paths.extend(pg)
    if paths:
        inc.append((game[0], paths))

# dir_list = match.listallfiles(mount + "/Users")
# for game in result:
#     paths = []
#     for path in game[1]:
#         matched = match.match_path(path, dir_list)
#         if matched:
#             paths.extend(matched)
#     if paths:
#         inc.append((game[0], paths))

for game in inc:
    print(game[0])
print(len(inc))
