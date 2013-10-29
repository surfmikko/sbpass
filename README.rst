Sparse Bundle Password Brute Force
==================================

These tools were created to recover password for OSX sparsebundle image, that I
just forgot. Implementation is rather naive and slow, about 6 pass/seconds with
Intel Core i5 1.8GHz / SSD disk. Mostly this will be effective only when there
is good clue about the password, that is your own passwords.

Generating wordlist is as simple as, writing all parts for formed password to
into a base wordlist `wordlist.base`. After this create full wordlist with
command::

    ./permutate.py wordlist.base > wordlist.txt

This will try to permutate good set of passwords from the base wordlist. You may
change the `MIN_WORD_LENGTH` variable to adjust duplicate word / good password
detection.

Now that you have wordlist ready, just start searching for password::

    ./sbpass.py wordlist.txt test-image.sparsebundle

This will try to detect good password with command `hditool imageinfo`. You
may change the amount of used threads with variable MAX_THREADS. When good
password is found, script just prints it and returns exit status 0. Otherwise
script returns with non-zero exit status.

