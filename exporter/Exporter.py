import os
import shutil

"""
Script to merge LCDA, L3T and ARKOpack mods into one

@author NicolasGrosjean
"""

def copytree(src, dst, symlinks=False, ignore=None):
    """Recursively copy a directory tree using copy2().

    The destination directory must not already exist.
    If exception(s) occur, an Error is raised with a list of reasons.

    If the optional symlinks flag is true, symbolic links in the
    source tree result in symbolic links in the destination tree; if
    it is false, the contents of the files pointed to by symbolic
    links are copied.

    The optional ignore argument is a callable. If given, it
    is called with the `src` parameter, which is the directory
    being visited by copytree(), and `names` which is the list of
    `src` contents, as returned by os.listdir():

        callable(src, names) -> ignored_names

    Since copytree() is called recursively, the callable will be
    called once for each directory that is copied. It returns a
    list of names relative to the `src` directory that should
    not be copied.

    XXX Consider this example code rather than the ultimate tool.

    """
    names = os.listdir(src)
    if ignore is not None:
        ignored_names = ignore(src, names)
    else:
        ignored_names = set()

    if not os.path.isdir(dst):  # Add this if to the original code
        os.makedirs(dst)
    errors = []
    for name in names:
        if name in ignored_names:
            continue
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                copytree(srcname, dstname, symlinks, ignore)
            else:
                # Will raise a SpecialFileError for unsupported file types
                shutil.copy2(srcname, dstname)
        # catch the Error from the recursive copytree so that we can
        # continue with other files
        except shutil.Error, err:
            errors.extend(err.args[0])
        except EnvironmentError, why:
            errors.append((srcname, dstname, str(why)))
    try:
        shutil.copystat(src, dst)
    except OSError, why:
        if WindowsError is not None and isinstance(why, WindowsError):
            # Copying file access times may fail on Windows
            pass
        else:
            errors.append((src, dst, str(why)))
    if errors:
        raise shutil.Error, errors

def main():
    LCDA_DIR = os.path.join('..', 'LCDA')
    ARKOpack_Armoiries_DIR = os.path.join('..', '..', 'ARKOpack', 'ARKOpack_Armoiries')
    ARKOpack_Interface_DIR = os.path.join('..', '..', 'ARKOpack', 'ARKOpack_Interface')
    L3T_DIR = os.path.join('..', '..', 'L3T', 'L3T')
    OUTPUT_DIR = os.path.join('..', 'LCDA_L3T_ARKOpack')

    # Delete the output if it already exists and create it again
    shutil.rmtree(OUTPUT_DIR) if os.path.isdir(OUTPUT_DIR) else None
    os.makedirs(OUTPUT_DIR)

    # TODO manage git branches

    if not os.path.isdir(ARKOpack_Armoiries_DIR):
        print('ARKOpack Armoiries mod directory not found')
    else:
        copytree(ARKOpack_Armoiries_DIR, OUTPUT_DIR)

    if not os.path.isdir(ARKOpack_Interface_DIR):
        print('ARKOpack Interface mod directory not found')
    else:
        copytree(ARKOpack_Interface_DIR, OUTPUT_DIR)

    if not os.path.isdir(L3T_DIR):
        print('L3T mod directory not found')
    else:
        copytree(L3T_DIR, OUTPUT_DIR)

    if not os.path.isdir(LCDA_DIR):
        print('LCDA mod directory not found')
    else:
        copytree(LCDA_DIR, OUTPUT_DIR)

if __name__ == '__main__':
    main()
