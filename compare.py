# compare files and file context in two directories
import os

def toFlag(function, *args, size=2):
    result = 0
    cur = 1
    for arg in args:
        if function(arg):result += cur
        cur *= size
    return result

def compare_files(file1, file2, files_diff):
    with open(file1,'rb') as f1, open(file2, 'rb') as f2:
        contents1=f1.read()
        contents2=f2.read()
        if contents1 != contents2:
            files_diff.write(file1+'\n')

def compare_dirs(dir1, dir2,file1_only, file2_only, files_diff, passConds=[]):
    """Compares two directories and prints any differences."""
    writer = [lambda x,y:file1_only.write(x+'\n'),lambda x,y:file2_only.write(y+'\n'),
	lambda x,y:compare_files(x,y, files_diff)]

    isLinkFlag = toFlag(os.path.islink, dir1, dir2)
    for i in range(2):
        if i+1 == isLinkFlag:
            writer[i](dir1, dir2)
            return
    if isLinkFlag==3:return
    isFileFlag = toFlag(os.path.isfile, dir1, dir2)

    for i in range(3):
        if i+1 == isFileFlag:
            writer[i](dir1, dir2)
            return    

    isExistFlag = toFlag(os.path.exists, dir1, dir2)
    for i in range(2):
        if i+1 == isExistFlag:
            writer[i](dir1, dir2)
            return
    files1 = os.listdir(dir1)
    files2 = os.listdir(dir2)

    set1 = set(files1)
    set2 = set(files2)

    union = set.union(set1,set2)
    for file in union:
        for cond in passConds:
            if cond(file):break
        else:compare_dirs(os.path.join(dir1,file),os.path.join(dir2,file), file1_only, file2_only, files_diff, passConds=passConds)

if __name__ == "__main__":
    # Get the two directories to compare.
    dir1 = 'qe-6.1-5'
    dir2 = 'q-e-qe-6.1.0'

    passConds = []
    passConds.append(lambda x:x.endswith('.o'))
    passConds.append(lambda x:x.endswith('.x'))
    passConds.append(lambda x:x.endswith('.mod'))

    curPath = os.path.dirname(os.path.abspath(__file__))
    print(curPath)#;exit()
    file1_only = open(curPath+'/'+dir1+'-only', 'w')
    file2_only = open(curPath+'/'+dir2+'-only', 'w')
    files_diff = open(curPath+'/dirs-diff', 'w')
    # Compare the two directories.
    compare_dirs(curPath+'/'+dir1, curPath+'/'+dir2, file1_only, file2_only, files_diff, passConds=passConds)
