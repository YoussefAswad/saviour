
import fnmatch
import os
# function to symlink files and folders caseinsensitively


def link_case_insensitive(src, dst):
    # get the absolute path to the source
    src = os.path.abspath(src)
    # get the absolute path to the destination
    dst = os.path.abspath(dst)
    # get the absolute path to the destination directory
    dst_dir = os.path.dirname(dst)
    # get the basename of the destination
    dst_basename = os.path.basename(dst)
    # get the list of files in the destination directory
    dst_dir_files = os.listdir(dst_dir)
    # get the list of files in the destination directory that match the destination basename
    dst_dir_files_match = fnmatch.filter(dst_dir_files, dst_basename)
    # if there is a match
    if dst_dir_files_match:
        # get the first match
        dst_dir_files_match = dst_dir_files_match[0]
        # get the absolute path to the first match
        dst_dir_files_match = os.path.join(dst_dir, dst_dir_files_match)
        # if the first match is a file
        if os.path.isfile(dst_dir_files_match):
            # if the source is a file
            if os.path.isfile(src):
                # symlink the source to the first match
                os.symlink(src, dst_dir_files_match)
        # if the first match is a directory
        elif os.path.isdir(dst_dir_files_match):
            # if the source is a directory
            if os.path.isdir(src):
                # symlink the source to the first match
                os.symlink(src, dst_dir_files_match)
    # if there is no match
    else:
        # if the source is a file
        if os.path.isfile(src):
            # symlink the source to the destination
            os.symlink(src, dst)
        # if the source is a directory
        elif os.path.isdir(src):
            # symlink the source to the destination
            os.symlink(src, dst)
