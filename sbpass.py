#!/usr/bin/python

# SETTINGS
MAX_THREADS = 20

import subprocess
import tempfile
import shutil
import sys
import threading
import time

PASSWORD_FOUND = False
SYSTEM_ERROR = False

class MyThread(threading.Thread):

    def __init__(self, password, sparsebundle):
        threading.Thread.__init__(self)
        self.password = password
        self.sparsebundle = sparsebundle

    def run(self):
        global PASSWORD_FOUND, SYSTEM_ERROR
        if PASSWORD_FOUND or SYSTEM_ERROR:
            return
        cmd = "hdiutil imageinfo -stdinpass %s" % self.sparsebundle
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        (stdout, stderr) = proc.communicate(self.password)
        if proc.returncode == 0:
            print "Password: %s" % self.password
            PASSWORD_FOUND=True
        elif stderr.find('Authentication error') == -1:
            if PASSWORD_FOUND or SYSTEM_ERROR:
                return
            print "Command returned unknown error:"
            print proc.returncode, stdout, stderr
            SYSTEM_ERROR=True

def write_process_status(password):
    statusfile = open('status', 'w')
    statusfile.write(password)
    statusfile.close()

def read_process_status():
    try:
        statusfile = open('status')
        first_password = statusfile.read()
        statusfile.close()
        return first_password
    except:
        return None

def main():
    wordlist = sys.argv[1]
    sparsebundle = sys.argv[2]

    count = 0
    start_time = 0
    total_lines = sum(1 for line in open(wordlist))

    first_password = read_process_status()

    f = open(wordlist)
    for password in f:

        count = count + 1
        if first_password != None:
            if password == first_password:
                first_password = None
            else:
                continue

        if PASSWORD_FOUND:
            exit(0)

        if SYSTEM_ERROR:
            exit(1)

        if count % 50 == 1:

            write_process_status(password)

            stop_time = time.time()
            passes_per_second = 50.0 / (stop_time - start_time)
            start_time = stop_time

            print "Trying (%i/%i %0.2f/sec): '%s'" % (count, total_lines,
                    passes_per_second, password.strip())

        thread = MyThread(password.strip(), sparsebundle)
        thread.start()

        while threading.activeCount() > MAX_THREADS:
            time.sleep(0.05)

    f.close()

    exit(1)

if __name__ == '__main__':
    main()
