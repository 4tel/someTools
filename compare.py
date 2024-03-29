# compare files and file context in two directories
import os

def compare_dirs(dir1, dir2,file1_only, file2_only, files_diff, passConds=[]):
    """Compares two directories and prints any differences."""
    isFile1 = os.path.isfile(dir1)
    isFile2 = os.path.isfile(dir2)
    if isFile1 and not isFile2:print(f"File {dir1} only exist.");file1_only.write(f'{dir1}\n');return
    if not isFile1 and isFile2:print(f"File {dir2} only exist.");file2_only.write(f'{dir2}\n');return
    if isFile1 and isFile2:
        with open(dir1, 'rb') as f1, open(dir2, 'rb') as f2:
            contents1 = f1.read()
            contents2 = f2.read()
            if contents1 != contents2:
                print(f"File {os.path.basename(dir1)} differs between the two directories.  {dir1}")
                files_diff.write(f'{dir1} {dir2} \n')
        return
    isExist1 = os.path.exists(dir1)
    isExist2 = os.path.exists(dir2)
    if isExist1 and not isExist2:print(f'File {dir1} only exist.');file1_only.write(f'{dir1}\n');return
    if not isExist1 and isExist2:print(f'File {dir2} only exist.');file2_only.write(f'{dir2}\n');return

    files1 = os.listdir(dir1)
    files2 = os.listdir(dir2)

    set1 = set(files1)
    set2 = set(files2)

    union = set.union(set1,set2)
    for file in union:
        for cond in passConds:
            if cond(file):
                break
        else:
            compare_dirs(os.path.join(dir1,file),os.path.join(dir2,file), file1_only, file2_only, files_diff)

if __name__ == "__main__":
    # Get the two directories to compare.
    dir1 = '6.1.5'
    dir2 = '6.1.0'

    passConds = []
    passConds.append(lambda x: not x.startswith('.'))

    curPath = os.path.relpath(os.path.dirname(__file__))
    file1_only = open(curPath+f'/{dir1}-only', 'w')
    file2_only = open(curPath+f'/{dir2}-only', 'w')
    files_diff = open(curPath+'/diff', 'w')

    # Compare the two directories.
    compare_dirs(dir1, dir2, file1_only, file2_only, files_diff)
