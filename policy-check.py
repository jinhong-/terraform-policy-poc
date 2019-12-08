from git import Repo
import os
from pathlib import Path
import fnmatch
import subprocess

stein_exe = 'stein'
target_branch = 'master'

file_exclusions = ['.policy/*']
valid_file_extensions = ['.hcl', '.tf', '.json', '.yml', '.yaml']

cwd = os.getcwd()
repo = Repo(cwd)
target_branch = repo.heads[target_branch]
diff = target_branch.commit.diff(repo.head.commit)

# Filter away items that are deleted
relevant_paths = [i.b_path for i in diff if i.change_type != 'D']

def is_valid_file(file):
    file = Path(file)    

    # Must match valid file extensions
    if(not any(map(lambda i: i == file.suffix.lower(), valid_file_extensions))):
        return False

    # Must not be present in file exclusions
    if(any(map(lambda p: fnmatch.fnmatch(file, p), file_exclusions))):
        return False

    return True

config_files = [p for p in relevant_paths if is_valid_file(p)]

subprocess.run([stein_exe, 'apply'] + config_files, shell=True, check=True)

# TODO: Redirect STD and Error output and write output to git PR