import os
import time
import hashlib

testfile = r"/home/tonton/Programmes_locaux/Tahoma2D/Tahoma2D.AppImage"
testfolder = r""

def check_file_size(filepath):
    start = time.time()

    size = os.path.getsize(filepath)

    end = time.time()
    etime = end-start
    return etime, size


def check_file_mod(filepath):
    start = time.time()

    mod = os.path.getmtime(filepath)

    end = time.time()
    etime = end-start
    return etime, mod


def check_file_checksum(filepath):
    start = time.time()

    checksum = hashlib.md5(open(filepath,'rb').read()).hexdigest()

    end = time.time()
    etime = end-start
    return etime, checksum

def check_file(filepath):
    print()
    print(f"Checking file : {filepath}")

    etime, size = check_file_size(filepath)
    print(f"Size : {size} - Time : {etime}")

    etime, mod = check_file_mod(filepath)
    print(f"ModD : {mod} - Time : {etime}")

    etime, chksum = check_file_checksum(filepath)
    print(f"Chks : {chksum} - Time : {etime}")

check_file(testfile)
