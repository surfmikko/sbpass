#!/usr/bin/python

# SETTINGS
MAX_THREADS = 20

import subprocess
import tempfile
import shutil
import sys
import threading
import time

class MyThread(threading.Thread):

    def __init__(self, password, sparsebundle):
        threading.Thread.__init__(self)
        self.password = password
        self.sparsebundle = sparsebundle

    def run(self):
        cmd = "hdiutil imageinfo -stdinpass %s" % self.sparsebundle
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        (stdout, stderr) = proc.communicate(self.password)
        if proc.returncode == 0:
            print "Password: %s" % self.password
            exit(0)

def main():
    wordlist = sys.argv[1]
    sparsebundle = sys.argv[2]

    count = 1
    start_time = 0
    total_lines = sum(1 for line in open(wordlist))

    f = open(wordlist)
    for password in f:

        if count % 50 == 1:
            stop_time = time.time()
            passes_per_second = 50 / (stop_time - start_time)
            start_time = stop_time
            print "Trying (%i/%i %i/sec): '%s'" % (count, total_lines,
                    passes_per_second, password.strip())
            
        thread = MyThread(password.strip(), sparsebundle)
        thread.start()

        while threading.activeCount() > MAX_THREADS:
            time.sleep(0.1)
        count = count + 1

    f.close()

    exit(1)

if __name__ == '__main__':
    main()
